import chess
from math import *

# watching
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

UI_OUT_DIR = "..\\uiOut";
UI_FEN_OUT = UI_OUT_DIR + "\\fen.txt";
UI_MOVE_OUT = UI_OUT_DIR + "\\move.txt";

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
        # check that UI and engine have the same board state
        with open(UI_FEN_OUT, "r") as file:
            uiFen = file.readline();
            if uiFen == "": return;
            if uiFen != self.board.fen():
                self.board.set_fen(uiFen);
        
        # push UI move
        with open(UI_MOVE_OUT, "r") as file:
            uiMove = file.readline();
            parseMove = self.board.parse_uci(uiMove);
            if uiMove == "" or not parseMove in self.board.legal_moves: return;
            self.board.push(parseMove);
        
        # go next
        print("making move");
        move, eval = minimaxPrune(self.board, 3, -inf, inf, self.board.turn);
        with open("..\\engineOut\\move.txt", "w+") as file:
            file.write(str(move));
        print("move made");

if __name__ == "__main__":
    # instance watchdog
    watcher = Observer();
    handler = EngineHandler();

    # schedule at uiOut directory
    watcher.schedule(handler, UI_OUT_DIR);
    watcher.start();
    
    # begin watching
    try:
        while watcher.is_alive():
            watcher.join(1);
    except KeyboardInterrupt:
        watcher.stop();
        watcher.join();
