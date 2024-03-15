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
sqS = floor(winS / 8);
transCol = "#abc123";

# picture displayed
class Board(chess.Board):
    def __init__(self):
        super().__init__();
    
    def writeDisplayPng(self):
        cairosvg.svg2png(bytestring=chess.svg.board(self), write_to=BUFF_PNG_FILE);

    def deleteDisplayPng(self):
        os.remove(BUFF_PNG_FILE);

# main window class
class Window(Tk):
    def __init__(self):
        super().__init__();
        self.geometry(str(winS) + "x" + str(winS));
        self.resizable(False, False);
        self.attributes("-transparentcolor", "white");
        
        # construct the label
        self.label = Label(self);
        self.label.pack();
        
    def drawBoard(self, board):
        # grabbing the display
        board.writeDisplayPng();
        
        # convert and resizing to viewport
        boardPng = Image.open(BUFF_PNG_FILE);
        boardPng = ImageTk.PhotoImage(boardPng.resize((winS, winS)));
        
        # draw the image
        self.label.config(image=boardPng);
        self.label.image = boardPng;
        board.deleteDisplayPng();

# converts move sequence to SAN representation
def sanM(move):
    return chess.Move.from_uci(move);

# handles the clicking of a piece
currM = ""; # stores current user move sequence
def handleClick(self, event):
    global currM;
    sqPos = chr(self.x + ord("a")) + str(8 - self.y);
    currM += sqPos;
    
    # check if move was made
    if len(currM) == 4:
        if sanM(currM) in board.legal_moves:
            print(currM);
        currM = "";

class Square(Frame):
    def __init__(self, master, i, j ):
        super().__init__(
            master=master,
            width=sqS,
            height=sqS,
            bg=transCol
        ); # initialise with checkered colour and square
        self.x = j; self.y = i; # saving x and y coordinates
        self.bind("<Button>", lambda event: handleClick(self, event));
        self.place(x=j * sqS);

class Row(Frame):
    def __init__(self, master, i):
        super().__init__(master=master, width=winS, height=sqS);
        for j in range(8):
            newSquare = Square(self, i, j);
        self.place(y=i * sqS);

if __name__ == "__main__":
    # initialise
    win = Window();
    
    # start the board
    board = Board();
    win.drawBoard(board);
    
    # initiliase each square
    for i in range(8):
        newRow = Row(win, i);
    
    win.mainloop();
    sys.exit(1); # Exits shellscript loop
