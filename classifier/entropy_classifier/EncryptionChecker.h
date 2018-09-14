#ifndef AES_SOFTWARE_ANALYZER_ENCRYPTIONCHECKER_H
#define AES_SOFTWARE_ANALYZER_ENCRYPTIONCHECKER_H


#include <cmath>
#include "Counter.h"
#include "Timer.h"


class EncryptionChecker {
public:
    EncryptionChecker(size_t fragmentSize,
                      int histogramThreshold,
                      double entropyThreshold,
                      Timer* timers,
                      Counter& typesCounter,
                      Counter& identificationResultCounter) noexcept;

    bool checkEncrypted(int encrypted, unsigned char* fragment) noexcept;

    void printSummary() noexcept;


private:
    int histogramThreshold;
    double entropyThreshold;
    size_t fragmentSize;
    Timer* timers;
    Counter typesCounter;
    Counter identificationResultCounter;
};


#endif //AES_SOFTWARE_ANALYZER_ENCRYPTIONCHECKER_H
