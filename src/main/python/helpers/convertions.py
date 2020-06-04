# Python code to demonstrate working
# of binary search in library
from bisect import bisect_left


def BinarySearch(a, x):
    i = bisect_left(a, x)
    if i:
        return i - 1
    else:
        return -1


def convert_bytes(size):
    types = ['B', 'KB', 'MB', 'GB', 'TB', 'TB', 'PB']
    dt_size = [10 ** 0, 10 ** 3, 10 ** 6, 10 ** 9, 10 ** 12, 10 ** 15, 10 ** 18]

    # Driver code
    idx = BinarySearch(dt_size, int(size))
    ret = dict()

    ret['type'] = types[idx]
    value = size / dt_size[idx]
    value = int(value * 100) / 100.0
    ret['value'] = value

    return ret
