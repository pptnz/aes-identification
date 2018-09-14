#ifndef AES_SOFTWARE_ANALYZER_DIRECTORY_H
#define AES_SOFTWARE_ANALYZER_DIRECTORY_H


#include <string>
#include <dirent.h>
#include <unistd.h>
#include <fcntl.h>
#include <climits>


class Directory {
public:
    explicit Directory(const std::string& directoryPath, int maxFragmentsCount) noexcept;

    bool getFragment(size_t fragmentSize, unsigned char* fragment) noexcept;

    void closeDirectory() noexcept;

    const int getProcessedFragmentsCount() const noexcept;


private:
    const std::string directoryPath;
    DIR* directory;
    int fileDescriptor;
    int processedFragmentsCount;
    int maxFragmentsCount;

    bool openNextFile() noexcept;
};


#endif //AES_SOFTWARE_ANALYZER_DIRECTORY_H
