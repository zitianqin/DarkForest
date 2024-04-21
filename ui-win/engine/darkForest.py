import chess
from math import *
from .helpers import *
from .eval import *
from .transTable import *
from .moveOrdering import *
from contextlib import redirect_stdout

STARTING_DEPTH = 3;

# evaluates a position recursively and return best move with evaluation
numPositions = 0;
bestMove = None;

# minimax algorithm with alpha(max), beta(min) pruning
def minimaxPrune(board, depth, ext, alp, bet, debugging):
    # terminal node so let's go back
    if depth == 0: return allEval(board);

    # constants
    global numPositions, bestMove;
    isPlayerWhite = board.turn;
    bestEval = -inf if isPlayerWhite else inf;
    orderedMoves = getOrderedMoves(board);
    numMoves = len(orderedMoves);
    evals = [];

    for move in orderedMoves:
        # temporary push and check that we have a bestMove
        if bestMove == None: bestMove = move;
        board.push(move);
        
        nextExt = 1 if (board.is_check() and ext == 0) else 0;

        # we're also gonna track the positions evaluated for debugging speed
        numPositions += 1;
        
        # not a very hard decision, my guy
        if numMoves == 1 and depth == STARTING_DEPTH:
            bestMove = move;
            eval, evals = allEval(board);
            if debugging: print(f"Only move, setting move {move} --> {evals} = {sum(evals)}");
            board.pop();
            return eval, evals;

        # if we find a terminal node
        if numMoves == 0:
            board.pop();
            # checkmate is not fun
            if board.is_check():
                # if the board is black to move then black killed white
                return inf*perspective(board), evals;
            else: # board is stalemate
                return 0, evals;
        
        # evaluate with Zobrist hashing
        hash = board.zobrist.getHash(board);
        hashExists = board.zobrist.hasHash(hash);
        if hashExists:
            if debugging: print(f"Found hash: {hex(hash)} with {move}");
            nextEval, nextEvals = board.zobrist.getEntry(hash);
        else:
            nextEval, nextEvals = minimaxPrune(board, depth - 1, nextExt, alp, bet, debugging);
        if debugging and depth >= 0:
            for i in range(STARTING_DEPTH - (depth + ext)): print("    ", end="");
            # color = "\x1B[38;2;255;0;0m" if board.turn else "\x1B[38;2;0;255;0m"
            print("White" if isPlayerWhite else "Black", end="");
            print(f"{nextEvals} = {nextEval} --> {move}");# \x1B[0m");

        # insert into Zobrist hash table (BROKEN)
        if not hashExists: board.zobrist.insertEntry(hash, [nextEval, nextEvals]);
        
        # we've found a more delicious move
        if (
                (not isPlayerWhite and bestEval > nextEval) or
                (isPlayerWhite and bestEval < nextEval)
            ):
            bestEval = nextEval;
            evals = nextEvals;
            if depth == STARTING_DEPTH:
                bestMove = move;
                if debugging: print(f"Natural, setting move {move} --> {evals} = {sum(evals)}");

        if isPlayerWhite:
            alp = max(alp, bestEval);
        else:
            bet = min(bet, bestEval);
        
        # undo move
        board.pop();

        # if alpha > beta then the move is bad and we prune
        if alp > bet:
            # if debugging: print(f"Pruning bad move, {move} with scores (a, b) = ({alp}, {bet})");
            break; # snip

    return bestEval, evals;

def callEngine(board, debugging):
    # go next
    global numPositions, bestMove;
    numPositions = 0;
    
    # debugFile = open("debug.txt", "w+");
    # with redirect_stdout(debugFile):
    for currDepth in range(STARTING_DEPTH, STARTING_DEPTH + 1):
        bestMove = None;
        eval, evals = minimaxPrune(board, currDepth, 0, -inf, inf, debugging);
        if debugging: print(f"Engine move made: {str(bestMove)}, {eval, evals} evaluated after {numPositions} positions");
    # debugFile.close();
    if debugging:  print("Table fill:", board.zobrist.numEntries);
    return bestMove;
