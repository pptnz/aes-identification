#include "Directory.h"

Directory::Directory(const std::string& directoryPath, int maxFragmentsCount) noexcept :
    directoryPath(directoryPath), processedFragmentsCount(0)
{
    if (maxFragmentsCount < 0) {
        this->maxFragmentsCount = INT_MAX;
    } else {
        this->maxFragmentsCount = maxFragmentsCount;
    }
    directory = opendir(directoryPath.c_str());
    openNextFile();
}


bool Directory::getFragment(size_t fragmentSize, unsigned char* fragment) noexcept {
    if (processedFragmentsCount >= maxFragmentsCount) {
        // reached full fragments
        return false;
    }

    ssize_t readSize = read(fileDescriptor, fragment, fragmentSize);
    bool openFileSuccess = false;
    while (readSize < fragmentSize) {
        close(fileDescriptor);
        openFileSuccess = openNextFile();
        if (!openFileSuccess) {
            // file exhausted
            return false;
        }

        readSize = read(fileDescriptor, fragment, fragmentSize);
    }

    processedFragmentsCount++;
    return true;
}


void Directory::closeDirectory() noexcept {
    close(fileDescriptor);
    closedir(directory);
}


const int Directory::getProcessedFragmentsCount() const noexcept {
    return processedFragmentsCount;
}


bool Directory::openNextFile() noexcept {
    struct dirent* directoryEntry = readdir(directory);

    while (true) {
        if (directoryEntry == nullptr) {
            // file exhausted
            return false;
        }

        if (directoryEntry->d_type != DT_REG || directoryEntry->d_name[0] == '.') {
            // not a normal file
            directoryEntry = readdir(directory);
            continue;
        }

        break;
    }

    // file found.
    std::string filePath = directoryPath + std::string(directoryEntry->d_name);
    fileDescriptor = open(filePath.c_str(), O_RDONLY);
    return true;
}
