import chess
import chess.svg
from tkinter import *
import sys
from PIL import Image, ImageTk
import os
from math import *
from constants import *
from helpers import *
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from io import BytesIO

# to track the current move
class MoveTracker():
	def __init__(self):
		self.value = "";
		
	def get(self):
		return self.value;
		
	def set(self, newM):
		self.value = newM;

# special button
class SpecBtn(Button):
	def __init__(self, master, text):
		pixel = PhotoImage(width=1, height=1)
		super().__init__(master, image=pixel, compound="c", text=text, width=BTN_WIDTH, height=BTN_HEIGHT);
		self.pack(side="left");

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
		
		svgData = chess.svg.board(self, fill=totalMapping,).encode("UTF-8");
		drawing = svg2rlg(BytesIO(svgData));
		renderPM.drawToFile(drawing, BUFF_PNG_FILE, fmt="PNG");

	# reset and redraw the board
	def resetWrapper(self, win):
		self.reset();
		win.reloadBoard();

	# when engine writes FEN to buff file, board changes to the FEN representation
	def loadEngineFen(self, win):
		with open(FEN_OUT_FILE, "r+") as out:
			try:
				fen = out.readline();
				self.set_fen(fen);
			except:
				print("Invalid engine FEN state");
		win.reloadBoard();
 
	# when engine writes move to buff file, board pushes move
	def loadEngineMove(self, win):
		with open(MOVE_OUT_FILE, "r+") as out:
			move = chess.Move.from_uci(out.readline());
			if move in self.legal_moves:
				self.push(move);
			else:
				print("Invalid engine move");
		win.reloadBoard();

# main window class
class Window(Tk):
	def __init__(self):
		super().__init__();
		self.title("DarkForest");
		self.config(bg=WIN_BG_COL); # for some reason no work
		self.wm_attributes("-transparentcolor", WIN_BG_COL);
		self.resizable(False, False); # for some reason no work
		self.geometry(str(winS) + "x" + str(winS + BTN_HEIGHT));
		
		# construct the display label
		self.label = Label(self, width=winS, height=winS);
		self.label.pack(fill="both", expand=True);
		self.label.bind("<Button>", lambda event: self.handleClick(event));
		
		# construct the move tracker
		self.cM = MoveTracker();

		# construct abstract board
		self.board = Board();
		self.reloadBoard();

		# construct button frame
		self.btns = Frame(self, width=winS, height=BTN_HEIGHT);
		self.btns.pack();

		# construct board reset button
		self.resetBoardBtn = SpecBtn(self.btns, "Reset");
		self.resetBoardBtn.bind("<Button>", lambda event: self.board.resetWrapper(self));

		# construct buttons that calls from engine's FEN output
		self.getEngineFenBtn = SpecBtn(self.btns, "Get FEN");
		self.getEngineFenBtn.bind("<Button>", lambda event: self.board.loadEngineFen(self));
		self.getEngineMoveBtn = SpecBtn(self.btns, "Get Move");
		self.getEngineMoveBtn.bind("<Button>", lambda event: self.board.loadEngineMove(self));

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
		winXOff = (self.winfo_width() - winS) / 2; # just in case the window gets resized
		winYOff = (self.winfo_height() - winS - BTN_HEIGHT) / 2;
		sqMOff = sqS - offset; # square side length without offset
		pixX = event.x - offset - winXOff; # calculate w/out the offset
		pixY = event.y - offset - winYOff;
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

	os.remove(BUFF_PNG_FILE); # remove any fluffy files
	sys.exit(1); # Exits shellscript loop
