import chess
import chess.svg
from tkinter import *
import sys
from PIL import Image, ImageTk
import cairosvg
import os
from math import *
from constants import *
from helpers import *

# to track the current move
class MoveTracker():
	def __init__(self):
		self.value = "";
		
	def get(self):
		return self.value;
		
	def set(self, newM):
		self.value = newM;

# picture displayed
class Board(chess.Board):
	def __init__(self):
		super().__init__();
		
	def writeDisplayPng(self, cM):
		# compute all the colourings
		selectedMapping = selectMap(self, cM);
		attackingMapping, movingMapping = attackMoveMap(self, cM);
		checkedKingMapping = checkMap(self);
		checkedMatedMapping = checkmateMap(self);
		staledMatedMapping = stalemateMap(self);
		
		totalMapping = {};
		for mapping in [
			selectedMapping,
			attackingMapping,
			movingMapping,
			checkedKingMapping,
			checkedMatedMapping,
			staledMatedMapping
		]:
			for key in mapping:
				totalMapping[key] = mapping[key];
		
		cairosvg.svg2png(
			bytestring=chess.svg.board(self, fill=totalMapping,),
			write_to=BUFF_PNG_FILE
		);

# main window class
class Window(Tk):
	def __init__(self):
		super().__init__();
		self.title("Cheese");
		self.geometry(str(winS) + "x" + str(winS));
		self.resizable(False, False);
		
		# construct the display label
		self.label = Label(self);
		self.label.pack();
		self.label.bind("<Button>", lambda event: self.handleClick(event));
		
		# construct the move tracker
		self.cM = MoveTracker();
		
		# construct abstract board
		self.board = Board();
		self.reloadBoard();
		
	def reloadBoard(self):
		# grabbing the display
		self.board.writeDisplayPng(self.cM);
		
		# convert and resizing to viewport
		boardPng = Image.open(BUFF_PNG_FILE);
		boardPng = ImageTk.PhotoImage(boardPng.resize((winS, winS)));
		
		# draw the image
		self.label.config(image=boardPng);
		self.label.image = boardPng;
			
	# handles the clicking of a piece
	def handleClick(self, event):
		global ratS, sqS;
		cM = self.cM.get();
		offset = sqS * ratS; # offset of black bars around board
		sqMOff = sqS - offset; # square side length without offset
		pixX = event.x - offset; # calculate w/out the offset
		pixY = event.y - offset;
		indX = floor(pixX / sqMOff); # calculate the indices of square
		indY = 8 - floor(pixY / sqMOff);

		# check for invalid moves
		if isOutOfBounds(indX + 1) or isOutOfBounds(indY):
			self.cM.set("");
			return;
		
		# now we append to user move
		sqPos = chr(indX + ord("a")) + str(indY);
		if sqPos == self.cM.get(): # also check for null move
			self.cM.set("");
			self.reloadBoard();
			return;
		cM += sqPos;
		
		# check if move was made
		if len(cM) == 4:
			sanCurrM = uciM(cM, self.board);
			
			# if legal we push
			if sanCurrM in self.board.legal_moves:
				self.board.push(sanCurrM);
			cM = "";
		self.cM.set(cM);
		self.reloadBoard();

if __name__ == "__main__":
	# initialise
	win = Window();
	win.mainloop();
		
	os.remove(BUFF_PNG_FILE); # remove and fluffy files
	sys.exit(1); # Exits shellscript loop
