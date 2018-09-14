#include "SettingsReader.h"


SettingsReader::SettingsReader(const std::string& settingsPath) noexcept {
    settingsFileStream = std::ifstream(settingsPath);
}


SettingsReader::~SettingsReader() noexcept {
    settingsFileStream.close();
}


void SettingsReader::readSettings(std::string* plainDirectoryPath,
                                  std::string* encryptedDirectoryPath,
                                  int* plainFragmentsCount,
                                  int* encryptedFragmentsCount,
                                  size_t* fragmentSize) noexcept {
    std::getline(settingsFileStream, *plainDirectoryPath);
    std::getline(settingsFileStream, *encryptedDirectoryPath);
    settingsFileStream >> *plainFragmentsCount;
    settingsFileStream >> *encryptedFragmentsCount;
    settingsFileStream >> *fragmentSize;
}
