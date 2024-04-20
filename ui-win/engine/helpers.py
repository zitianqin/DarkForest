import chess
from math import *

# if white then positive, if black then negative
def perspective(board):
    return (1 if board.turn else -1);

# merge sort for move: eval dictionary
def merge(arr, lo, mid, hi):
    leftLen = mid - lo + 1;
    rightLen = hi - mid - 1;
    
    # copy arr
    left = arr[slice(lo, lo + leftLen)];
    right = arr[slice(mid + 1, mid + 1 + rightLen)];
    i = j = 0; k = lo;
    
    # merging time
    while i < leftLen and j < rightLen:
        if left[i][1] > right[j][1]:
            arr[k] = left[i];
            i += 1;
        else:
            arr[k] = right[j];
            j += 1;
        k += 1;
    
    # copy the rest
    while i < leftLen:
        arr[k] = left[i];
        i += 1;
        k += 1;
    while j < rightLen:
        arr[k] = right[j];
        j += 1;
        k += 1;

def mergeSort(arr, lo, hi):
    if lo < hi:
        mid = int(floor((lo + hi)/2));
        mergeSort(arr, lo, mid);
        mergeSort(arr, mid + 1, hi);
        merge(arr, lo, mid, hi);
    return arr;
