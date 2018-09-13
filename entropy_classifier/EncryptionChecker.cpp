#include "EncryptionChecker.h"


EncryptionChecker::EncryptionChecker(size_t fragmentSize,
                                     int histogramThreshold,
                                     double entropyThreshold,
                                     Timer* timers,
                                     Counter& typesCounter,
                                     Counter& identificationResultCounter) noexcept :
        fragmentSize(fragmentSize),
        histogramThreshold(histogramThreshold),
        entropyThreshold(entropyThreshold),
        timers(timers), typesCounter(typesCounter), identificationResultCounter(identificationResultCounter) {}


bool EncryptionChecker::checkEncrypted(int encrypted, unsigned char* fragment) noexcept {
    timers[0].start();
    timers[1].start();
    timers[2].start();
    timers[3].start();

    int histogram[256] = {0};
    for (int& hist: histogram) {
        hist = 0;
    }
    for (int i = 0; i < fragmentSize; i++) {
        histogram[fragment[i]]++;
    }

    double entropy = 0;
    for (const int hist: histogram) {
        if (hist >= histogramThreshold) {
            timers[0].stop();
            timers[1].stop();
            typesCounter.countLabel(0);
            identificationResultCounter.countLabel(encrypted);
            return false;
        }

        if (hist != 0) {
            entropy += hist * log2(hist);
        }
    }

    if (entropy >= entropyThreshold) {
        timers[0].stop();
        timers[2].stop();
        typesCounter.countLabel(1);
        identificationResultCounter.countLabel(encrypted);
        return false;
    }

    timers[0].stop();
    timers[3].stop();
    typesCounter.countLabel(2);
    identificationResultCounter.countLabel(encrypted + 1);
    return true;
}


void EncryptionChecker::printSummary() noexcept {
    // Set Name
    typesCounter.setLabelName(0, "SkippedByHistogram");
    typesCounter.setLabelName(1, "SkippedByEntropy");
    typesCounter.setLabelName(2, "Encrypted");

    identificationResultCounter.setLabelName(0, "True Negative");
    identificationResultCounter.setLabelName(1, "False Positive");
    identificationResultCounter.setLabelName(2, "False Negative");
    identificationResultCounter.setLabelName(3, "True Positive");

    // Compute result table
    double trueNegative = 0;
    double falsePositive = 0;
    double falseNegative = 0;
    double truePositive = 0;

    auto identificationResult = identificationResultCounter.getCounts();

    double plainFragmentsCount = identificationResult[0] + identificationResult[1];
    if (plainFragmentsCount > 0) {
        trueNegative = identificationResult[0] / plainFragmentsCount * 100;
        falsePositive = identificationResult[1] / plainFragmentsCount * 100;
    }

    double encryptedFragmentsCount = identificationResult[2] + identificationResult[3];
    if (encryptedFragmentsCount > 0) {
        falseNegative = identificationResult[2] / encryptedFragmentsCount * 100;
        truePositive = identificationResult[3] / encryptedFragmentsCount * 100;
    }

    double accuracy = (identificationResult[0] + identificationResult[3])
                      / (plainFragmentsCount + encryptedFragmentsCount)
                      * 100;

    // Print summary
    std::cout << "Fragments: " << std::endl;
    printf("Plain: %d, Encrypted: %d\n", (int)plainFragmentsCount, (int)encryptedFragmentsCount);

    std::cout << "\nResult:" << std::endl;
    printf("%6.2lf%%\t%6.2lf%%\n%6.2lf%%\t%6.2lf%%\n", trueNegative, falsePositive, falseNegative, truePositive);
    printf("=> Accuracy: %6.2lf%%\n", accuracy);

    std::cout << "\nFragments:" << std::endl;
    identificationResultCounter.print();

    std::cout << "\nType:" << std::endl;
    typesCounter.print();

    std::cout << "\nTime:" << std::endl;
    timers[0].print();
    timers[1].print();
    timers[2].print();
    timers[3].print();
}