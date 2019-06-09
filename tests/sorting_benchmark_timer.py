import os, sys
from abc import ABCMeta, abstractmethod
from random import sample
import copy
from collections import OrderedDict

from time import time
from functools import wraps

###################
# timer decorator #
###################

def timefn(fn):
    """Simple timer decorator."""
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time()
        result = fn(*args, **kwargs)
        t2 = time()
        print(f"@timefn: {fn.__name__} \
            took {str(t2 - t1)} seconds")
        return result
    return measure_time

SAMPLE_SIZE = {
    'micro' :5,
    'small' :100,       # 10**2
    'medium':1000,      # 10**3
    'large' :100000,    # 10**5
    'xlarge':1000000    # 10**6
}

SAMPLE_DATA = OrderedDict()

########
# main #
########

@timefn
def main():

    sample_limit = 'xlarge'

    if len(sys.argv) > 1:
        if sys.argv[1] in SAMPLE_SIZE.keys():
            sample_limit = sys.argv[1]
    
    # sample data generation
    print("- sample data generation ...")
    for k, v in SAMPLE_SIZE.items():
        SAMPLE_DATA[k] = sample(range(0, v), v)
        print(" > %s - %d"%(k, len(SAMPLE_DATA[k])))

        if k == sample_limit:
            break

    # quick sort benchmark
    print("- quick sort benchmark ...")
    quick_sort_bench()

    # merge sort benchmark
    print("- merge sort benchmark ...")
    merge_sort_bench()

#############
# benchmark #
#############

@timefn
def quick_sort_bench():

    sample_data = copy.deepcopy(SAMPLE_DATA)

    for k in SAMPLE_DATA:
        print(" > %s - quick sort"%(k))
        sort(SAMPLE_DATA[k], sort_type='quick')

@timefn
def merge_sort_bench():

    sample_data = copy.deepcopy(SAMPLE_DATA)

    for k in SAMPLE_DATA:
        print(" > %s - merge sort"%(k))
        sort(SAMPLE_DATA[k], sort_type='merge')

#####################
# sorting algorithm #
#####################

@timefn
def sort(data, sort_type):

    if sort_type == "quick":
        quick_sort(data)
    elif sort_type == "merge":
        merge_sort(data)
    else:
        raise NotImplementedError()

def quick_sort(arr):

    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    lesser_arr, equal_arr, greater_arr = [], [], []
    for num in arr:
        if num < pivot:
            lesser_arr.append(num)
        elif num > pivot:
            greater_arr.append(num)
        else:
            equal_arr.append(num)
    return quick_sort(lesser_arr) + equal_arr + quick_sort(greater_arr)

def merge_sort(arr):

    if len(arr) < 2:
        return arr

    mid = len(arr) // 2
    low_arr = merge_sort(arr[:mid])
    high_arr = merge_sort(arr[mid:])

    merged_arr = []
    l = h = 0
    while l < len(low_arr) and h < len(high_arr):
        if low_arr[l] < high_arr[h]:
            merged_arr.append(low_arr[l])
            l += 1
        else:
            merged_arr.append(high_arr[h])
            h += 1
    merged_arr += low_arr[l:]
    merged_arr += high_arr[h:]
    return merged_arr

if __name__ == "__main__":
    main()
