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

BUFF_PNG_FILE = "buff.png";

class Board(chess.Board):
    def __init__(self):
        super().__init__();
    
    def writeDisplayPng(self):
        cairosvg.svg2png(bytestring=chess.svg.board(self), write_to=BUFF_PNG_FILE);

    def deleteDisplayPng(self):
        os.remove(BUFF_PNG_FILE);

class Window(Tk):
    def __init__(self, file_path):
        super().__init__();
        self.size = int(pag.size()[1] * 2 / 3)
        self.geometry(str(self.size) + "x" + str(self.size));
        
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
    
if __name__ == "__main__":
    win = Window("chessboard.svg");
    board = Board();
    win.drawBoard(board);
    win.mainloop();
