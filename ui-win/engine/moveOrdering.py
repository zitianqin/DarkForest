import chess
from .helpers import *
from .eval import *

# evaluate first and orders the board's list of legal moves to shorten the search
def getOrderedMoves(board):
    scale = 10; # scale accounts for 10*pawn > queen
    orderedMoves = {};
    legalMoves= board.legal_moves;
    for move in legalMoves:
        guessVal = 0;
        
        fromSq = move.from_square;
        fromPc = board.piece_at(fromSq);
        toSq = move.to_square;
        toPc = board.piece_at(move.to_square);
        
        # captures
        if toPc != None:
            guessVal += scale*values[toPc.piece_type] - values[fromPc.piece_type];

        # promotions
        if move.promotion != None:
            if board.turn and chess.square_rank(fromSq) == 6:
                guessVal += scale*values[move.promotion];
            if not board.turn and chess.square_rank(fromSq) == 2:
                guessVal += scale*values[move.promotion];        
        
        orderedMoves[move] = guessVal;
    
    # merge 
    sortedArr = list(orderedMoves.items())
    sortedArr = mergeSort(sortedArr, 0, legalMoves.count());

    # filter out moves
    sortedMoves = [];
    for obj in sortedArr:
        sortedMoves.append(obj[0]);
    return sortedMoves;
