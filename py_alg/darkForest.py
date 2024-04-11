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

def evaluate(board):
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
    
    # white is true
    return (whiteEval - blackEval) * (1 if board.turn else -1);

def evaluateRec(board, depth):
    if (depth == 0):
        return evaluate(board);
    
    maxEval = -inf;
    for move in board.legal_moves:
        board.push(move);
        maxEval = max(maxEval, evaluateRec(board, depth - 1));
        board.pop();

    return maxEval;

if __name__ == "__main__":
    board = chess.Board();
    print(evaluateRec(board, 4));
