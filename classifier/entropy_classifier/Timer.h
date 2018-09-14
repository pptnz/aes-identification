#ifndef AES_SOFTWARE_ANALYZER_TIMER_H
#define AES_SOFTWARE_ANALYZER_TIMER_H


#include <cstdio>
#include <string>
#include <chrono>


class Timer {
public:
    explicit Timer(const std::string& name, size_t fragmentSize) noexcept;

    void start() noexcept;

    void stop() noexcept;

    void reset() noexcept;

    void print() const noexcept;

    double fragmentsPerSecond() const noexcept;

    double speedInMB() const noexcept;


private:
    std::string name;
    std::chrono::high_resolution_clock::time_point startPoint;
    std::chrono::nanoseconds elapsedTime;
    int processedFragmentsCount;
    size_t fragmentSize;
};


#endif //AES_SOFTWARE_ANALYZER_TIMER_H
