import chess
from math import *
from helpers import *

# watching
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

UI_OUT_DIR = "..\\uiOut";
UI_FEN_OUT = UI_OUT_DIR + "\\fen.txt";
UI_MOVE_OUT = UI_OUT_DIR + "\\move.txt";
STARTING_DEPTH = 4;

# evaluates a position recursively and return best move with evaluation
numPositions = 0;
def minimaxPrune(board, depth, alp, bet):
    if (depth == 0):
        return evalPcVal(board), board.peek();
    
    # iterate
    global numPositions;
    bestMove = None;
    for move in board.legal_moves:
        numPositions += 1;
        
        # push
        board.push(move);
        if hasRepeatedMoves(board): # generally don't want repetition
            board.pop();
            continue;
        
        # evaluate
        nextEval, nextMove = minimaxPrune(board, depth - 1, -bet, -alp); # we don't care about next moves which we can't make
        nextEval += numCoverSquares(board, move.to_square); # coverage
        nextEval += centreCtrlVal(board, move.to_square); # centre control
        nextEval *= -1; # opponent's best move is bad for us
        board.pop();
        
        # pruning and check that we have a best move
        if bestMove == None or alp <= nextEval:
            bestMove = move;
        alp = max(alp, nextEval);
        if (nextEval >= bet):
            return bet, bestMove;

    return -alp, bestMove;

lastUiMove = None; # make sure we're somehow not repeating moves
class EngineHandler(LoggingEventHandler):
    def __init__(self):
        super().__init__();
        self.board = chess.Board();
    
    def on_modified(self, event):
        if (event.src_path == UI_FEN_OUT): return;
        
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
            watcher.join(0.5);
    except KeyboardInterrupt:
        watcher.stop();
        watcher.join();
