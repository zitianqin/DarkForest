import chess
import chess.svg
from tkinter import *
import tksvg
import pyautogui as pag
import keyboard as kb
import sys
from PIL import Image, ImageTk
from svglib.svglib import svg2rlg
import cairosvg
import os
from math import *

BUFF_PNG_FILE = "buff.png";

winS = int(pag.size()[1] * 2 / 3);
ratS = 0.245;
winClickRat = 1.23; # scaling up viewport to mouse click
sqS = winS * winClickRat / 8;

# picture displayed
class Board(chess.Board):
    def __init__(self):
        super().__init__();
    
    def writeDisplayPng(self):
        cairosvg.svg2png(bytestring=chess.svg.board(self), write_to=BUFF_PNG_FILE);

# converts move sequence to SAN representation
currM = ""; # stores current user move sequence
def sanM(move):
    return chess.Move.from_uci(move);

# main window class
class Window(Tk):
    def __init__(self):
        super().__init__();
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
        
        # now we append to user move
        sqPos = chr(indX + ord("a")) + str(indY);
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
