#include "Counter.h"


Counter::Counter(int labelsCount) noexcept {
    for (int i = 0; i < labelsCount; i++) {
        counts.emplace_back(0);
        labelNames.emplace_back("noname");
    }
}


void Counter::setLabelName(int label, const std::string& labelName) noexcept {
    labelNames[label] = labelName;
}


void Counter::countLabel(int label) noexcept {
    counts[label]++;
}


void Counter::print() const noexcept {
    double total = 0;
    for (int count: counts) {
        total += count;
    }

    for (int i = 0; i < counts.size(); i++) {
        printf("%s: %d (%6.2lf%%)\n", labelNames[i].c_str(), counts[i], counts[i] / total * 100);
    }
}


const std::vector<int>& Counter::getCounts() const noexcept {
    return counts;
}
