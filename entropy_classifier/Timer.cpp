#include "Timer.h"


Timer::Timer(const std::string& name, size_t fragmentSize) noexcept :
    name(name), elapsedTime(std::chrono::nanoseconds::zero()),
    fragmentSize(fragmentSize), processedFragmentsCount(0) { }


void Timer::start() noexcept {
    startPoint = std::chrono::high_resolution_clock::now();
}


void Timer::stop() noexcept {
    auto endPoint = std::chrono::high_resolution_clock::now();
    processedFragmentsCount++;
    elapsedTime += std::chrono::duration_cast<std::chrono::nanoseconds>(endPoint - startPoint);
}


void Timer::reset() noexcept {
    elapsedTime = std::chrono::nanoseconds::zero();
}


void Timer::print() const noexcept {
    long long int totalTime = elapsedTime.count();

    int formattedTimes[4];
    for (int& formattedTime: formattedTimes) {
        formattedTime = (int)(totalTime % 1000);
        totalTime /= 1000;
    }

    printf("%s: %d.%03d.%03d.%03d secs\n",
            name.c_str(),
            formattedTimes[3],
            formattedTimes[2],
            formattedTimes[1],
            formattedTimes[0]);
    printf("\t%.2lf fragments / sec\n", fragmentsPerSecond());
    printf("\t%.2lf MB / sec\n", speedInMB());
}


double Timer::fragmentsPerSecond() const noexcept {
    return (double)processedFragmentsCount * 1000000000 / elapsedTime.count();

}


double Timer::speedInMB() const noexcept {
    return fragmentsPerSecond() * fragmentSize / (1 << 20);
}
