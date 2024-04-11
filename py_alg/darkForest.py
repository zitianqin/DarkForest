import chess
from math import *

# watching
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, LoggingEventHandler

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

class EngineHandler(LoggingEventHandler):
    def __init__(self):
        super().__init__();
        self.board = chess.Board();
    
    def on_modified(self, event):
        move, eval = minimaxPrune(self.board, 4, -inf, inf, chess.WHITE);
        with open("..\\engineOut\\move.txt", "w+") as file:
            file.write(str(move));

if __name__ == "__main__":
    # instance watchdog
    watcher = Observer();
    handler = LoggingEventHandler();

    # schedule at uiOut directory
    UI_OUT_DIR = "..\\uiOut";
    watcher.schedule(handler, UI_OUT_DIR);
    watcher.start();
    
    # begin watching
    try:
        while watcher.is_alive():
            watcher.join(1);
    except KeyboardInterrupt:
        watcher.stop();
        watcher.join();
