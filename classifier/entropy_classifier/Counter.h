#ifndef AES_SOFTWARE_ANALYZER_COUNTER_H
#define AES_SOFTWARE_ANALYZER_COUNTER_H


#include <iostream>
#include <string>
#include <vector>


class Counter {
public:
    explicit Counter(int labelsCount) noexcept;

    void setLabelName(int label, const std::string& labelName) noexcept;

    void countLabel(int label) noexcept;

    void print() const noexcept;

    const std::vector<int>& getCounts() const noexcept;


private:
    std::vector<int> counts;
    std::vector<std::string> labelNames;
};


#endif //AES_SOFTWARE_ANALYZER_COUNTER_H
