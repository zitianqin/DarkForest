import chess
from math import *

values = {
    "p": 1,
    "k": 0,
    "q": 10,
    "b": 3,
    "n": 3,
    "r": 5,
}

def evaluate(board, player):
    boardFen = str(board.board_fen());
    
    # white eval
    whiteEval = 0;
    for c in boardFen:
        if ord("A") <= ord(c) and ord(c) <= ord("Z"):
            lowerC = chr(ord(c) + ord("a") - ord("A"));
            whiteEval += values[lowerC];
    
    # black eval
    blackEval = 0;
    for c in boardFen:
        if ord("a") <= ord(c) and ord(c) <= ord("z"):
            blackEval += values[c];
    
    return whiteEval - blackEval;

# evaluates a position recursively and return best move with evaluation
def minimaxPrune(board, depth, alp, bet, player):
    if (depth == 0):
        return None, evaluate(board, player);
    
    isWhite = player == chess.WHITE;
    bestEval = -inf if isWhite else inf;
    compareFunc = (max if isWhite else min);
    bestMove = None;
    
    # iterate
    for move in board.legal_moves:
        # check that we have a returning move
        if bestMove == None: bestMove = move;
        
        # push and evaluate
        board.push(move);
        nextMove, nextEval = minimaxPrune(board, depth - 1, alp, bet, not player);
        board.pop();

        # we've found a better move
        if nextEval != bestEval: bestMove = move;
        bestEval = compareFunc(bestEval, nextEval);
        
        # pruning
        if isWhite:
            alp = compareFunc(alp, bestEval);
            if alp > bestEval: break;
        else:
            bet = compareFunc(bet, bestEval);
            if bet < bestEval: break;

    return bestMove, bestEval;

if __name__ == "__main__":
    board = chess.Board();
    state = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
    board.set_fen(state);
    move, eval = minimaxPrune(board, 4, -inf, inf, chess.WHITE);
    print(str(move));
