import chess
import chess.svg
from tkinter import *
import sys
from PIL import Image, ImageTk
import cairosvg
import os
from math import *
from constants import *

# picture displayed
class Board(chess.Board):
    def __init__(self):
        super().__init__();
    
    def writeDisplayPng(self):
        cairosvg.svg2png(bytestring=chess.svg.board(self), write_to=BUFF_PNG_FILE);

# converts move sequence to SAN representation
def sanM(move):
    return chess.Move.from_uci(move);

# main window class
class Window(Tk):
    def __init__(self):
        super().__init__();
        self.title("Cheese");
        self.geometry(str(winS) + "x" + str(winS));
        self.resizable(False, False);
        
        # construct the label
        self.label = Label(self);
        self.label.pack();
        self.label.bind("<Button>", lambda event: self.handleClick(event));
        
        # construct abstract board
        self.board = Board();
        self.drawBoard();
        
    def drawBoard(self):
        # grabbing the display
        self.board.writeDisplayPng();
        
        # convert and resizing to viewport
        boardPng = Image.open(BUFF_PNG_FILE);
        boardPng = ImageTk.PhotoImage(boardPng.resize((winS, winS)));
        
        # draw the image
        self.label.config(image=boardPng);
        self.label.image = boardPng;
            
    # handles the clicking of a piece
    def handleClick(self, event):
        global ratS, sqS, currM;
        offset = sqS * ratS; # offset of black bars around board
        sqMOff = sqS * (1 - ratS); # square side length without offset
        pixX = event.x - offset; # calculate w/out the offset
        pixY = event.y - offset;
        indX = floor(pixX / sqMOff); # calculate the indices of square
        indY = 8 - floor(pixY / sqMOff);

        # check for invalid moves
        if (not (1 <= indX and indX <= 8)) or (not (1 <= indY and indY <= 8)):
            currM = "";
            return;
        
        # now we append to user move
        sqPos = chr(indX + ord("a")) + str(indY);
        if sqPos == currM: # also check for null move
            currM = ""
            return;
        currM += sqPos;
        
        # check if move was made
        if len(currM) == 4:
            sanCurrM = sanM(currM);
            if sanCurrM in self.board.legal_moves:
                self.board.push_san(str(sanCurrM));
                self.drawBoard();
            currM = "";

if __name__ == "__main__":
    # initialise
    win = Window();
    
    win.mainloop();
    os.remove(BUFF_PNG_FILE); # remove and fluffy files
    sys.exit(1); # Exits shellscript loop
