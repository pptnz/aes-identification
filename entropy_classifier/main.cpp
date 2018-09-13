#include "Directory.h"
#include "Timer.h"
#include "Counter.h"
#include "EncryptionChecker.h"
#include "SettingsReader.h"

int main() {
    // Read settings
    std::string plainDirectoryPath;
    std::string encryptedDirectoryPath;
    int plainFragmentsCount = 0;
    int encryptedFragmentsCount = 0;
    size_t fragmentSize = 0;
    SettingsReader settingsReader("./settings.txt");
    settingsReader.readSettings(&plainDirectoryPath, &encryptedDirectoryPath,
                                &plainFragmentsCount, &encryptedFragmentsCount, &fragmentSize);

    // Make logger
    Timer timer0("ElapsedTime", fragmentSize);
    Timer timer1("HistogramSkipped", fragmentSize);
    Timer timer2("EntropySkipped", fragmentSize);
    Timer timer3("Encrypted", fragmentSize);
    Timer timers[4] = {timer0, timer1, timer2, timer3};
    Counter typesCounter(3);
    Counter identificationResultCounter(4);

    // Make EncryptionChecker
    EncryptionChecker encryptionChecker(fragmentSize,
                                        55, 16700.0,
                                        timers, typesCounter, identificationResultCounter);

    // Make fragment variables
    unsigned char fragment[fragmentSize];

    // Test Plain Fragments
    std::cout << "Testing Plain Fragments." << std::endl;
    Directory plainDirectory(plainDirectoryPath, plainFragmentsCount);
    while ((plainDirectory.getFragment(fragmentSize, fragment))) {
        encryptionChecker.checkEncrypted(0, fragment);

        if (plainDirectory.getProcessedFragmentsCount() % 100000 == 0) {
            std::cout << "\t" << plainDirectory.getProcessedFragmentsCount() << " fragments tested." << std::endl;
        }
    }
    plainDirectory.closeDirectory();

    // Test Encrypted Fragments
    std::cout << "\nTesting Encrypted Fragments." << std::endl;
    Directory encryptedDirectory(encryptedDirectoryPath, encryptedFragmentsCount);
    while ((encryptedDirectory.getFragment(fragmentSize, fragment))) {
        encryptionChecker.checkEncrypted(2, fragment);

        if (encryptedDirectory.getProcessedFragmentsCount() % 100000 == 0) {
            std::cout << "\t" << encryptedDirectory.getProcessedFragmentsCount() << " fragments tested." << std::endl;
        }
    }
    encryptedDirectory.closeDirectory();

    // Print summary
    std::cout << "\n======= Result =======" << std::endl;
    encryptionChecker.printSummary();

    // Terminate
    return 0;
}