#ifndef AES_SOFTWARE_ANALYZER_SETTINGSREADER_H
#define AES_SOFTWARE_ANALYZER_SETTINGSREADER_H


#include <string>
#include <fstream>


class SettingsReader {
public:
    explicit SettingsReader(const std::string& settingsPath) noexcept;

    ~SettingsReader() noexcept;

    void readSettings(std::string* plainDirectoryPath,
                      std::string* encryptedDirectoryPath,
                      int* plainFragmentsCount,
                      int* encryptedFragmentsCount,
                      size_t* fragmentSize) noexcept;


private:
    std::ifstream settingsFileStream;
};


#endif //AES_SOFTWARE_ANALYZER_SETTINGSREADER_H
