#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdarg.h>
#include <unistd.h>
#include <fcntl.h>
#include <dirent.h>
#include <limits.h>
#include <iterator>
#include <numeric>
#include <iostream>

#undef __ARM_NEON__
#undef __ARM_NEON
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#define __ARM_NEON__
#define __ARM_NEON

#include "../interface/xi_interface.hpp"
#include "../interface/xi_readwrite_util.hpp"
#include "sds_lib.h"



// -------------------------------------------
// -------------- Namespaces------------------
// -------------------------------------------
using namespace std;



// --------------------------------------------
// ---------------- Types ---------------------
// --------------------------------------------
typedef signed char int8_t;



// --------------------------------------------
// ----------- Global Variables ---------------
// --------------------------------------------
DIR* dir;



// -------------------------------------------
// --------------- Macros --------------------
// -------------------------------------------
#define TIME_START (clockStart = sds_clock_counter());
#define TIME_STOP { \
	clockEnd = sds_clock_counter(); \
	updateTotalTime(); \
}
#define ConvertToFP(fVal, iPart, fbits)	((int)((iPart<<fbits) + ((fVal-(float)iPart))*(1<<fbits)))



// -------------------------------------------
// ---------- Class Declarations -------------
// -------------------------------------------
class Timer {
public:
    Timer();
    void start();
    void stop();
    double getTotalTime_msec();
    double getTotalTime_sec();
    double msecPerFragment(int totalFragmentsCount);
    double fragmentsPerSecond(int totalFragmentsCount);

private:
    long long startClock;
    long long clockFrequency;
    double totalTime_msec;    
};



// -------------------------------------------
// --------- Function Declarations -----------
// -------------------------------------------
bool toSkip(float* histogram, int maxThreshold);
void loadFragment(float* histogram, float mean, int8_t* buff_ptr, io_layer_info ioLayerInfoPtr);
bool checkEncrypted(float* result, float threshold);
void printResult(float* unpackedOutput);
void printLog(const char* msgType, const char* msg, ...);
void printNewLine();
string getNextFileName();
bool getNextHistogram(const char* directoryPath, float* histogram);



// -------------------------------------------
// --------- Main Routine --------------------
// -------------------------------------------
int main(int argc, char **argv) {
    // Paths to use
    char* dirpath = "/mnt/models/AESNet";
    char* caffemodel = "model.caffemodel";
    char* prototxt = "deploy.prototxt";

    // Layer Information
    string startLayer = "";
    string endLayer = "";
    bool isFirstLayer = 1;
    int numImgToProcess = 2;
    float mean = 15.9547;

    // Struct which holds the input/output layer info
    io_layer_info ioLayerInfoPtr;

    // Init call
    void* chaihandle = xiInit(dirpath, prototxt, caffemodel, &ioLayerInfoPtr,
                              numImgToProcess, isFirstLayer, startLayer, endLayer);

    // Create buffer for unpacked input
    void* ptr;
    vector<void*> normalizeInput;
    for (int batchId = 0; batchId < numImgToProcess; batchId++) {
        ptr = malloc(768 * sizeof(int8_t));
        normalizeInput.push_back(ptr);
    }

    // Create buffer for packed input
    int inSize = ioLayerInfoPtr.inlayer_sizebytes;
    vector<void*> input;
    for (int i = 0; i < ioLayerInfoPtr.num_in_bufs; i++) {
        if (ioLayerInfoPtr.inlayer_exectype.compare("hardware") == 0) {
            ptr = sds_alloc_non_cacheable(inSize);
        } else {
            ptr = malloc(inSize);
        }
        input.push_back(ptr);
    }

    // Create buffer for packed output
    int outSize = ioLayerInfoPtr.outlayer_sizebytes;
    vector<void*> output;
    for (int i = 0; i < ioLayerInfoPtr.num_out_bufs; i++) {
        if (ioLayerInfoPtr.outlayer_exectype.compare("hardware") == 0) {
            ptr = sds_alloc_non_cacheable(outSize);
        } else {
            ptr = malloc(outSize);
        }
        output.push_back(ptr);
    }

    // Create buffer for unpacked output
    int unpackOutSize = ioLayerInfoPtr.outlayer_sizebytes;
    vector<void*> unpackedOutput;
    for (int batchId = 0; batchId < numImgToProcess; batchId++) {
        ptr = malloc(unpackOutSize);
        unpackedOutput.push_back(ptr);
    }

    // Loading required params for unpack function
    kernel_type_e outKerType = ioLayerInfoPtr.out_kerType;
    int outLayerSize = ioLayerInfoPtr.out_size;

    // Variables for testing
    float histogram[256] = {0};
    int plainFragmentsCount = 0;
    int plainCorrectCount = 0;
    double plainAccuracy = 0;
    int encryptedFragmentsCount = 0;
    int encryptedCorrectCount = 0;
    double encryptedAccuracy = 0;
    int totalFragmentsCount = 0;
    int totalCorrectCount = 0;
    double totalAccuracy = 0;
    int numFragmentsToTest = 0;
    int skippedPlainCount = 0;
    int skippedEncryptedCount = 0;
    Timer totalTimer;
    Timer plainTimer;
    Timer plainSkipTimer;
    Timer plainNetTimer;
    Timer encryptedTimer;
    Timer encryptedSkipTimer;
    Timer encryptedNetTimer;
    printLog("TESTPARAM", "Number of fragments to test (0 to full test): ");
    scanf("%d", &numFragmentsToTest);
    if (numFragmentsToTest <= 0) {
        numFragmentsToTest = INT_MAX;
    }
    printNewLine();

    // Testing Plain Fragments
    printLog("TEST", "Testing Plain Fragments. Please Wait...");
    dir = opendir("/mnt/plain/");
    while (true) {
        if (plainFragmentsCount % 1000 == 0) {
            printLog("TEST", "%d plain fragments tested.", plainFragmentsCount);
        }

        totalTimer.start();
        plainTimer.start();
        plainSkipTimer.start();
        plainNetTimer.start();

        // Load Histogram
        if (!getNextHistogram("/mnt/plain/", histogram)) {
            break;
        }

        // Preprocess without neural network
        if (toSkip(histogram, 55)) {
            totalTimer.stop();
            plainTimer.stop();
            plainSkipTimer.stop();

            plainFragmentsCount++;
            skippedPlainCount++;
            plainCorrectCount++;

            if (plainFragmentsCount >= numFragmentsToTest) {
               break;
            }
            
            continue;
        }

        // Normalize Input
        loadFragment(histogram, mean, (int8_t*)normalizeInput[0], ioLayerInfoPtr);

        // load input
        xiInputRead(normalizeInput, input, numImgToProcess, ioLayerInfoPtr);

        // execute inference		
        xiExec(chaihandle, input, output);

        // unpacks the output data		
        xiUnpackOutput(output, unpackedOutput, outKerType, outLayerSize, numImgToProcess);

        totalTimer.stop();
        plainTimer.stop();
        plainNetTimer.stop();

        // Write the output data to txt file
        plainFragmentsCount++;
        if (!checkEncrypted((float*)(unpackedOutput[0]), 0.1)) {
            plainCorrectCount++;
        }

        if (plainFragmentsCount >= numFragmentsToTest) {
            break;
        }
    }
    printNewLine();

    // Testing Encrypted Fragments
    printLog("TEST", "Testing Encrypted Fragments. Please Wait...");
    closedir(dir);
    dir = opendir("/mnt/encrypted/");
    while (true) {
        if (encryptedFragmentsCount % 1000 == 0) {
            printLog("TEST", "%d encrypted fragments tested.", encryptedFragmentsCount);
        }

        totalTimer.start();
        encryptedTimer.start();
        encryptedSkipTimer.start();
        encryptedNetTimer.start();

        // Load Histogram
        if (!getNextHistogram("/mnt/encrypted/", histogram)) {
            break;
        }

        // Preprocess without neural network
        if (toSkip(histogram, 55)) {
            totalTimer.stop();
            encryptedTimer.stop();
            encryptedSkipTimer.stop();

            encryptedFragmentsCount++;
            skippedEncryptedCount++;

            if (encryptedFragmentsCount >= numFragmentsToTest) {
               break;
            }

            continue;
        }

        // Normalize Input
        loadFragment(histogram, mean, (int8_t*)normalizeInput[0], ioLayerInfoPtr);

        // load input
        xiInputRead(normalizeInput, input, numImgToProcess, ioLayerInfoPtr);

        // execute inference		
        xiExec(chaihandle, input, output);

        // unpacks the output data		
        xiUnpackOutput(output, unpackedOutput, outKerType, outLayerSize, numImgToProcess);

        totalTimer.stop();
        encryptedTimer.stop();
        encryptedNetTimer.stop();

        // Write the output data to txt file
        encryptedFragmentsCount++;
        if (checkEncrypted((float*)(unpackedOutput[0]), 0.1)) {
            encryptedCorrectCount++;
        }

        if (encryptedFragmentsCount >= numFragmentsToTest) {
            break;
        }
    }
    printNewLine();

    // Print result
    totalFragmentsCount = plainFragmentsCount + encryptedFragmentsCount;
    totalCorrectCount = plainCorrectCount + encryptedCorrectCount;
    plainAccuracy = (double)plainCorrectCount / plainFragmentsCount * 100;
    encryptedAccuracy = (double)encryptedCorrectCount / encryptedFragmentsCount * 100;
    totalAccuracy = (double)totalCorrectCount / totalFragmentsCount * 100;
    printLog("RESULT", "Plain: %d / %d (%6.2lf%%)", plainCorrectCount, plainFragmentsCount, plainAccuracy);
    printLog("RESULT", "Encrypted: %d / %d (%6.2lf%%)", encryptedCorrectCount, encryptedFragmentsCount, encryptedAccuracy);
    printLog("RESULT", "Total: %d / %d (%6.2lf%%)", totalCorrectCount, totalFragmentsCount, totalAccuracy);
    printNewLine();

    double skippedPlainRate = (double)skippedPlainCount / plainFragmentsCount * 100;
    double skippedEncryptedRate = (double)skippedEncryptedCount / encryptedFragmentsCount * 100;
    printLog("SKIP", "Plain Skipped: %d / %d (%6.2lf%%)", skippedPlainCount, plainFragmentsCount, skippedPlainRate);
    printLog("SKIP", "Encrypted Skipped: %d / %d (%6.2lf%%)", skippedEncryptedCount, encryptedFragmentsCount, skippedEncryptedRate);
    printNewLine();

    // Print Timing Result
    printLog("TIME", "Total: %6.2lf secs", totalTimer.getTotalTime_sec());
    printLog("TIME", "\t%7.4lf msecs / fragment", totalTimer.msecPerFragment(totalFragmentsCount));
    printLog("TIME", "\t%7.2lf fragments / sec", totalTimer.fragmentsPerSecond(totalFragmentsCount));
    printLog("TIME", "\tSpeed: %6.2lf MB / sec", totalTimer.fragmentsPerSecond(totalFragmentsCount) / 256);
    printNewLine();

    printLog("TIME", "Plain: %6.2lf secs", plainTimer.getTotalTime_sec());
    printLog("TIME", "\t%7.4lf msecs / fragment", plainTimer.msecPerFragment(plainFragmentsCount));
    printLog("TIME", "\t%7.2lf fragments / sec", plainTimer.fragmentsPerSecond(plainFragmentsCount));
    printLog("TIME", "\tSpeed: %6.2lf MB / sec", plainTimer.fragmentsPerSecond(plainFragmentsCount) / 256);
    printNewLine();

    printLog("TIME", "Encrypted: %6.2lf secs", encryptedTimer.getTotalTime_sec());
    printLog("TIME", "\t%7.4lf msecs / fragment", encryptedTimer.msecPerFragment(encryptedFragmentsCount));
    printLog("TIME", "\t%7.2lf fragments / sec", encryptedTimer.fragmentsPerSecond(encryptedFragmentsCount));
    printLog("TIME", "\tSpeed: %6.2lf MB / sec", encryptedTimer.fragmentsPerSecond(encryptedFragmentsCount) / 256);
    printNewLine();

    printLog("TIME", "Skipped Plain: %6.2lf secs", plainSkipTimer.getTotalTime_sec());
    printLog("TIME", "\t%7.4lf msecs / fragment", plainSkipTimer.msecPerFragment(skippedPlainCount));
    printLog("TIME", "\t%7.2lf fragments / sec", plainSkipTimer.fragmentsPerSecond(skippedPlainCount));
    printLog("TIME", "\tSpeed: %6.2lf MB / sec", plainSkipTimer.fragmentsPerSecond(skippedPlainCount) / 256);
    printNewLine();

    printLog("TIME", "Skipped Encrypted: %6.2lf secs", encryptedSkipTimer.getTotalTime_sec());
    printLog("TIME", "\t%7.4lf msecs / fragment", encryptedSkipTimer.msecPerFragment(skippedEncryptedCount));
    printLog("TIME", "\t%7.2lf fragments / sec", encryptedSkipTimer.fragmentsPerSecond(skippedEncryptedCount));
    printLog("TIME", "\tSpeed: %6.2lf MB / sec", encryptedSkipTimer.fragmentsPerSecond(skippedEncryptedCount) / 256);
    printNewLine();

    printLog("TIME", "Net Plain: %6.2lf secs", plainNetTimer.getTotalTime_sec());
    printLog("TIME", "\t%7.4lf msecs / fragment", plainNetTimer.msecPerFragment(plainFragmentsCount - skippedPlainCount));
    printLog("TIME", "\t%7.2lf fragments / sec", plainNetTimer.fragmentsPerSecond(plainFragmentsCount - skippedPlainCount));
    printLog("TIME", "\tSpeed: %6.2lf MB / sec", plainNetTimer.fragmentsPerSecond(plainFragmentsCount - skippedPlainCount) / 256);
    printNewLine();

    printLog("TIME", "Net Encrypted: %6.2lf secs", encryptedNetTimer.getTotalTime_sec());
    printLog("TIME", "\t%7.4lf msecs / fragment", encryptedNetTimer.msecPerFragment(encryptedFragmentsCount - skippedEncryptedCount));
    printLog("TIME", "\t%7.2lf fragments / sec", encryptedNetTimer.fragmentsPerSecond(encryptedFragmentsCount - skippedEncryptedCount));
    printLog("TIME", "\tSpeed: %6.2lf MB / sec", encryptedNetTimer.fragmentsPerSecond(encryptedFragmentsCount - skippedEncryptedCount) / 256);
    printNewLine();

    // Call Release
    xiRelease(chaihandle);

    // Release buffers
    for (int batchId = 0; batchId < normalizeInput.size(); batchId++) {
        free(normalizeInput[batchId]);
    }

    for (int i = 0; i < input.size(); i++) {
        sds_free(input[i]);
    }

    for (int i = 0; i < output.size(); i++) {
        sds_free(output[i]);
    }

    for (int batchId = 0; batchId < unpackedOutput.size(); batchId++) {
        free(unpackedOutput[batchId]);
    }

    // Terminate
    return 0;
}



// -------------------------------------------
// ----------- Class Definitions -------------
// -------------------------------------------
Timer::Timer() {
    startClock = 0;
    clockFrequency = sds_clock_frequency();
    totalTime_msec = 0;
}


void Timer::start() {
    startClock = sds_clock_counter();
}


void Timer::stop() {
    long long clockTime = sds_clock_counter() - startClock;
    totalTime_msec += (double)(clockTime) / clockFrequency * 1000;
}


double Timer::getTotalTime_msec() {
    return totalTime_msec;
}


double Timer::getTotalTime_sec() {
    return totalTime_msec / 1000;
}


double Timer::msecPerFragment(int totalFragmentsCount) {
    return totalTime_msec / totalFragmentsCount;
}


double Timer::fragmentsPerSecond(int totalFragmentsCount) {
    return totalFragmentsCount / totalTime_msec * 1000;    
}



// -------------------------------------------
// --------- Function Definitions ------------
// -------------------------------------------
bool toSkip(float* histogram, int maxThreshold) {
    for (int i = 0; i < 256; i++) {
        if (histogram[i] >= maxThreshold) {
            return true;
        }
    }
    return false;
}


void loadFragment(float* histogram, float mean, int8_t* buff_ptr, io_layer_info ioLayerInfoPtr) {
    // Load input layer params
    int inBw = ioLayerInfoPtr.in_bw;
    int inHeight = ioLayerInfoPtr.in_height;
    int inWidth = ioLayerInfoPtr.in_width;
    int inChannel = ioLayerInfoPtr.in_channel;
    int inFbits = ioLayerInfoPtr.in_fbits;

    // Maximum Positive and Negative
    int maxPositive = ((1 << (inBw - 1)) - 1);
    int maxNegative = -(1 << (inBw - 1));

    // Local variables to use
    IO_DATA_TYPE ival = 0;
    int uncappedFxval = 0;
    IO_DATA_TYPE fxval = 0;
    int histogramIndex = 0;
    int bufferIndex = 0;
    float data = 0;

    for (int h = 0; h < inHeight; h++) {
        for (int w = 0; w < inWidth; w++) {
            // compute data to cap
            data = histogram[histogramIndex] - mean;
            ival = (int)data;
            uncappedFxval = ConvertToFP(data, ival, inFbits);

            // cap the data
            if (uncappedFxval > maxPositive) {
                fxval = maxPositive;
            } else if (uncappedFxval < maxNegative) {
                fxval = maxNegative;
            } else {
                fxval = uncappedFxval;
            }

            // commit to result
            buff_ptr[bufferIndex] = fxval;
            bufferIndex += inChannel;
            histogramIndex++;
        }
    }
}


bool checkEncrypted(float* result, float threshold) {
    if (result[1] >= threshold) {
        return true;
    } else {
        return false;
    }
}


void printResult(float* unpackedOutput) {
    char label = checkEncrypted(unpackedOutput, 0.1) ? 'O' : 'X';
    printLog("RESULT", "%6.2f%% %6.2f%% (%c)", unpackedOutput[0] * 100, unpackedOutput[1] * 100, label);
}


void printLog(const char* msgType, const char* msg, ...) {
    cout << "[" << msgType << "] ";
    va_list args;
    va_start(args, msg);
    vprintf(msg, args);
    va_end(args);
    cout << endl;
}


void printNewLine() {
    cout << endl;
}


string getNextFileName() {
    struct dirent* ent;

    while ((ent = readdir(dir)) != NULL) {
        char* filename = ent->d_name;
        if (filename[0] == '.') {
            continue;
        }
        return filename;
    }

    return "";
}


bool getNextHistogram(const char* directoryPath, float* histogram) {
    static string filePath = directoryPath + getNextFileName();
    static int fd = open(filePath.c_str(), O_RDONLY);

    unsigned char buffer[4096];
    int count = read(fd, buffer, 4096);

    while (count < 4096) {
        close(fd);

        filePath = directoryPath + getNextFileName();
        if (filePath == directoryPath) {
            return false;
        }

        fd = open(filePath.c_str(), O_RDONLY);
        count = read(fd, buffer, 4096);
    }

    for (int i = 0; i < 256; i++) {
        histogram[i] = 0;
    }
    for (int i = 0; i < 4096; i++) {
        histogram[buffer[i]]++;
    }

    return true;
}
