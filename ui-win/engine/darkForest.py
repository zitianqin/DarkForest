import chess
from math import *
from .helpers import *
from .eval import *
from .transTable import *

STARTING_DEPTH = 4;

# evaluates a position recursively and return best move with evaluation
numPositions = 0;
bestMove = None;

# minimax algorithm with alpha(max), beta(min) pruning
def minimaxPrune(board, depth, alp, bet):
    # terminal node so let's go back
    if depth == 0: return allEval(board);

    # constants
    global numPositions, bestMove;
    bestEval = -inf if board.turn == chess.WHITE else inf;
    legMs = board.legal_moves;
    evals = [];

    for move in legMs:
        # temporary push and check that we have a bestMove
        if bestMove == None: bestMove = move;
        board.push(move);

        # we're also gonna track the positions evaluated for debugging speed
        numPositions += 1;
        # not a very hard decision, my guy
        if legMs.count() == 1:
            if depth == STARTING_DEPTH:
                bestMove = move;
                print(f"Setting move {move} --> {evals} = {sum(evals)}");
            eval = allEval(board);
            board.pop();
            return eval;

        # if we already find a checkmate
        if board.is_checkmate() and depth == STARTING_DEPTH:
            board.pop();
            bestMove = move;
            print(f"Setting move {move} --> {evals} = {sum(evals)}");
            # if the board is black then black is dead
            return inf if board.turn == chess.BLACK else -inf, [];

        # temporary push and evaluate with Zobrist hashing
        hash = zobristHash(board);
        hashExists = hasTableEntry(hash);
        nextEval, evals = getEntry(hash) if hashExists else minimaxPrune(board, depth - 1, alp, bet);
        for i in range(STARTING_DEPTH - depth): print("    ", end="");
        print(f"{evals} = {nextEval} --> {move}");

        # insert into Zobrist hash table
        if not hashExists:
            insertEntry(hash, (nextEval, evals));
        
        # we've found a more delicious move
        if (
                (board.turn == chess.WHITE and bestEval > nextEval) or
                (board.turn == chess.BLACK and bestEval < nextEval)
            ):
            bestEval = nextEval;
            if depth == STARTING_DEPTH:
                bestMove = move;
                print(f"Setting move {move} --> {evals} = {sum(evals)}");

        if board.turn == chess.WHITE: # not actually black's turn
            alp = max(alp, nextEval);
        else:
            bet = min(bet, nextEval);
        
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
    eval, evals = minimaxPrune(board, STARTING_DEPTH, -inf, inf);
    print(f"Engine move made: {str(bestMove)}, {eval, evals} evaluated after {numPositions} positions");
    return bestMove;
