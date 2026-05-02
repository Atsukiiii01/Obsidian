import math
from collections import Counter


def shannon_entropy(data):
    if not data:
        return 0.0

    freq = Counter(data)
    total = len(data)
    entropy = 0.0

    for count in freq.values():
        p = count / total
        entropy -= p * math.log2(p)

    return entropy
