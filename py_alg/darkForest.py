import chess
from math import *
from helpers import *
from transTable import *

# watching
import os
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

UI_OUT_DIR = "..\\uiOut";
UI_FEN_OUT = UI_OUT_DIR + "\\fen.txt";
UI_MOVE_OUT = UI_OUT_DIR + "\\move.txt";
STARTING_DEPTH = 3;

# evaluates a position recursively and return best move with evaluation
numPositions = 0;
bestMove = None;
def minimaxPrune(board, depth, alp, bet):
    if (depth == 0):
        return allEval(board);
    
    # iterate
    global numPositions, bestMove;
    orderedLegMoves = orderMovesByGuess(board);
    for move in orderedLegMoves:
        # not a very hard decision, my guy and also think less if there's less moves to make
        numLegM = numLegalMoves(board);
        if numLegM == 1: return allEval(board);
        depth = int(ceil(depth * (1 - (1/numLegM))));
        numPositions += 1;
        
        # push and evaluate
        board.push(move);
        nextEval = -round(minimaxPrune(board, depth - 1, -bet, -alp), 4);
        
        # pruning 
        if alp < nextEval:
            # check that we have a best move
            if depth == STARTING_DEPTH or bestMove == None:
                bestMove = move;
            # v0 = evalPcVal(board);
            # v1 = evalOwnCheck(board);
            # v2 = captureEval(board);
            # v3 = numCoverSquares(board, move.to_square);
            # v4 = centreCtrlVal(board, move.to_square);
            # v5 = transEval(board) / 100;
            # print(f"new best move {move} //// {v0}, {v1}, {v2}, {v3}, {v4}, {v5}, {v0+v1+v2+v3+v4+v5}");
            alp = nextEval;
        board.pop();

        if (nextEval >= bet) and not isinf(bet):
            return bet;
    return alp;

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
        global numPositions, bestMove;
        numPositions = 0;
        eval = minimaxPrune(self.board, STARTING_DEPTH, -inf, inf);
        if bestMove == None: return;
        with open("..\\engineOut\\move.txt", "w+") as file:
            file.write(str(bestMove));
        print(f"Engine move made: {str(bestMove)}, {eval} evaluated after {numPositions} positions");

if __name__ == "__main__":
    # instance watchdog
    watcher = Observer();
    handler = EngineHandler();

    # schedule at uiOut directory
    watcher.schedule(handler, UI_OUT_DIR);
    watcher.start();
    
    # begin watching
    os.system("cls");
    try:
        while watcher.is_alive():
            watcher.join();
    except KeyboardInterrupt:
        watcher.stop();
        watcher.join();
