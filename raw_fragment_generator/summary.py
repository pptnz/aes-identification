import numpy as np


def summary(fragment, fragment_size):
    byte_values = np.zeros(fragment_size)
    byte_frequency_distribution = np.zeros(256)
    low_ascii_frequency = 0
    medium_ascii_frequency = 0
    high_ascii_frequency = 0

    for i in range(fragment_size):
        binary_value = fragment[i]
        byte_values[i] = binary_value
        byte_frequency_distribution[binary_value] += 1
        if binary_value < 31:
            low_ascii_frequency += 1
        elif binary_value < 127:
            medium_ascii_frequency += 1
        else:
            high_ascii_frequency += 1

    mean_byte_values = np.mean(byte_values)
    difference = byte_values - mean_byte_values
    std_byte_values = np.std(byte_values)
    mean_absolute_deviation = np.mean(np.absolute(difference))

    standarized_kurtosis = np.sum(np.power(difference, 4)) / ((std_byte_values ** 4 + 1) * (fragment_size - 1))
    standarized_skewness = np.sum(np.power(difference, 3)) / ((std_byte_values ** 3 + 1) * (fragment_size - 1))
    average_contiguity_between_bytes = np.sum(np.power(difference, 4)) / (np.sum(np.power(difference, 2)) ** 2 + 1)
    maximum_byte_streak = np.max(byte_frequency_distribution)

    frequencies = np.array([low_ascii_frequency, medium_ascii_frequency, high_ascii_frequency])

    result = byte_frequency_distribution.tolist() + \
             [mean_byte_values, std_byte_values, mean_absolute_deviation] + \
             [standarized_kurtosis, standarized_skewness, average_contiguity_between_bytes, maximum_byte_streak] + \
             frequencies.tolist()

    return result
