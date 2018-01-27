def summary(fragment, fragment_size):
    binary_frequency_distribution = [0 for _ in range(256)]

    for i in range(fragment_size):
        binary_frequency_distribution[fragment[i]] += 1

    return binary_frequency_distribution
