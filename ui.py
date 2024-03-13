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
        self.size = int(pag.size()[1] * 2 / 3)
        self.geometry(str(self.size) + "x" + str(self.size));
        self.resizable(False, False);
        
        # construct the label
        self.label = Label(self);
        self.label.pack();
        
    def drawBoard(self, board):
        # grabbing the display
        board.writeDisplayPng();
        
        # convert and resizing to viewport
        boardPng = Image.open(BUFF_PNG_FILE);
        boardPng = ImageTk.PhotoImage(boardPng.resize((self.size, self.size)));
        
        # draw the image
        self.label.config(image=boardPng);
        self.label.image = boardPng;
        board.deleteDisplayPng();

# handles the clicking of a piece
def handleClick(event):
    print(str(event.x), str(event.y));

class Square(Frame):
    def __init__(self, master, size, i, j ):
        colours = ["white", "black"];
        side = floor(size / 8);
        super().__init__(
            master=master,
            width=side,
            height=side,
            background=colours[(i + j) % 2]
        ); # initialise with checkered colour and square
        self.x = j; self.y = i; # saving x and y coordinates
        self.bind("<Enter>", lambda event: handleClick);
        self.place(x=j * side);

class Row(Frame):
    def __init__(self, master, size, i):
        super().__init__(master=master, width=size, height=floor(size / 8));
        for j in range(8):
            newSquare = Square(self, size, i, j);
        self.place(y=i * floor(size / 8));

if __name__ == "__main__":
    # initialise
    win = Window();
    
    # start the board
    board = Board();
    win.drawBoard(board);

    # initiliase each square
    colours = ["black", "white"];
    for i in range(8):
        newRow = Row(win, win.size, i);
    
    win.mainloop();
    sys.exit(1); # Exits shellscript loop
