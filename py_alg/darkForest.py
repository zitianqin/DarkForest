import chess
from math import *

# watching
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

UI_OUT_DIR = "..\\uiOut";
UI_FEN_OUT = UI_OUT_DIR + "\\fen.txt";
UI_MOVE_OUT = UI_OUT_DIR + "\\move.txt";
STARTING_DEPTH = 3;

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
    
    return (whiteEval - blackEval) * (1 if board.turn == chess.WHITE else -1);

# evaluates a position recursively and return best move with evaluation
numPositions = 0;
def minimaxPrune(board, depth, alp, bet):
    if (depth == 0):
        return evaluate(board), None;
    
    # iterate
    global numPositions;
    bestMove = None;
    for move in board.legal_moves:
        numPositions += 1;
        if (numPositions % 1000 == 0): print(numPositions);
        
        # push and evaluate
        board.push(move);
        nextEval, nextMove = minimaxPrune(board, depth - 1, -bet, -alp);
        nextEval *= -1; # opponent's best move is bad for us
        board.pop();
        
        # pruning and check that we have a best move
        if bestMove == None or alp != nextEval: bestMove = move;
        alp = max(alp, nextEval);
        if (nextEval > bet):
            return bet, bestMove;

    return -alp, bestMove;

lastUiMove = None; # make sure we're somehow not repeating moves
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
            global lastUiMove;
            if uiMove == "" or lastUiMove == uiMove:
                return;
            else:
                lastUiMove = uiMove;
            
            try:
                parseMove = self.board.parse_uci(uiMove);
                self.board.push(parseMove);
                print("Move made by UI:", uiMove);
            except Exception as e:
                print("Error:", e);
        
        # go next
        global numPositions;
        numPositions = 0;
        eval, move = minimaxPrune(self.board, STARTING_DEPTH, -inf, inf);
        if move == None: return;
        with open("..\\engineOut\\move.txt", "w+") as file:
            file.write(str(move));
        print("Engine move made:", str(move), ", evaluated after ", numPositions, " positions");

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
