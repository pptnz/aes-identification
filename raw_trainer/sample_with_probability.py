import random


def sample_with_probability(probability):
    if random.random() < probability:
        return True
    return False
