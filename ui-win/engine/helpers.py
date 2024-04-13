import chess
from math import *

# what do you think this does :)
def numLegalMoves(board):
    numM = 0;
    for move in board.legal_moves:
        numM += 1;
    return numM;

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

# evaluate first and orders the board's list of legal moves to shorten the search
def orderMovesByGuess(board):
    return board.legal_moves;
    orderedMoves = {};
    legalMoves= board.legal_moves;
    for move in legalMoves:
        board.push(move);
        orderedMoves[move] = allEval(board);
        board.pop();
    
    # merge sort
    mergeSort(list(orderedMoves.items()), 0, numLegalMoves(board));
    return list(orderedMoves.keys());
