import chess
from math import *
from .helpers import *
from .eval import *
from .transTable import *

STARTING_DEPTH = 2;

# evaluates a position recursively and return best move with evaluation
numPositions = 0;
bestMove = None;

# minimax algorithm with alpha(max), beta(min) pruning
def minimaxPrune(board, depth, ext, alp, bet):
    # terminal node so let's go back
    if depth + ext == 0: return allEval(board);

    # constants
    global numPositions, bestMove;
    isPlayerWhite = board.turn;
    bestEval = -inf if isPlayerWhite else inf;
    legMs = board.legal_moves;
    evals = [];
    newPcVal = 0;

    for move in legMs:
        # temporary push and check that we have a bestMove
        if bestMove == None: bestMove = move;
        board.push(move);
        
        if ext != 1 and board.is_check(): ext = 1; # simple search extension

        # we're also gonna track the positions evaluated for debugging speed
        numPositions += 1;
        # not a very hard decision, my guy
        if legMs.count() == 1:
            if depth == STARTING_DEPTH:
                bestMove = move;
                print(f"Only move, setting move {move} --> {evals} = {sum(evals)}");
            eval = allEval(board);
            board.pop();
            return eval;

        # if we already find a checkmate
        if board.is_checkmate() and depth == STARTING_DEPTH:
            board.pop();
            bestMove = move;
            print(f"Checkmate, setting move {move} --> {evals} = {sum(evals)}");
            # if the board is black to move then black killed white
            return -inf if not isPlayerWhite else inf, evals;

        # evaluate with Zobrist hashing
        hash = zobristHash(board);
        hashExists = hasTableEntry(hash);
        nextEval, nextEvals = getEntry(hash) if hashExists else minimaxPrune(board, depth - 1, ext, alp, bet);
        if depth >= 0 and len(nextEvals) > 0 and (newPcVal != nextEvals[0]):
            newPcVal = nextEvals[0];
            for i in range(STARTING_DEPTH - (depth + ext)): print("    ", end="");
            color = "\x1B[38;2;255;0;0m" if board.turn else "\x1B[38;2;0;255;0m"
            print(f"{color}{nextEvals} = {nextEval} --> {move}\x1B[0m");

        # insert into Zobrist hash table
        if not hashExists: insertEntry(hash, (nextEval, nextEvals));
        
        # we've found a more delicious move
        if (
                (not isPlayerWhite and bestEval > nextEval) or
                (isPlayerWhite and bestEval < nextEval)
            ):
            bestEval = nextEval;
            evals = nextEvals;
            if depth == STARTING_DEPTH:
                bestMove = move;
                print(f"Natural, setting move {move} --> {evals} = {sum(evals)}");

        if isPlayerWhite:
            alp = max(alp, bestEval);
        else:
            bet = min(bet, bestEval);
        
        # undo move
        board.pop();

        # if alpha > beta then the move is bad and we prune
        if alp > bet: break; # snip

    return bestEval, evals;

def callEngine(board):
    # go next
    global numPositions, bestMove;
    numPositions = 0;
    bestMove = None;
    clearTable();
    
    for currDepth in range(0, STARTING_DEPTH + 1):
        eval, evals = minimaxPrune(board, currDepth, 0, -inf, inf);
        print(f"Engine move made: {str(bestMove)}, {eval, evals} evaluated after {numPositions} positions");
    return bestMove;
