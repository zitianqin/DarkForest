import os
from math import *
from constants import *
from helpers import *

# GUI
import chess
import chess.svg
from tkinter import *

# SVG <-> PNG images for display
from PIL import Image, ImageTk
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from io import BytesIO

# engine interfacing
from engine.darkForest import *
from engine.transTable import *

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
	def __init__(self, master, text, command):
		super().__init__(master, image=PhotoImage(), compound="center", text=text, width=BTN_WIDTH, height=BTN_HEIGHT);
		self.bind("<Button>", command);
		self.pack(side="left");

# picture displayed
class Board(chess.Board):
	def __init__(self):
		super().__init__();
  
		# initialise Zobrist
		self.zobrist = Zobrist();
		
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
		pngData = BytesIO();
		drawing = svg2rlg(BytesIO(svgData));
		renderPM.drawToFile(drawing, pngData, fmt="PNG");
		return pngData;

	# reset and redraw the board
	def resetWrapper(self, win):
		self.reset();
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
		self.resetBoardBtn = SpecBtn(self.btns, "Reset", lambda event: self.board.resetWrapper(self));

		# construct button that toggles calls from engine's FEN output
		self.engineBtn = SpecBtn(self.btns, "Start engine", lambda event: self.toggleEngine(self.engineBtn));
		self.engineOn = False;
  
		# construct button that sets FEN
		self.setFenBtn = SpecBtn(self.btns, "Set FEN board state\n(CAREFUL)", lambda event: self.readSetFen());

	def reloadBoard(self):
		# grab, open display and resize to viewport
		boardPng = Image.open(self.board.writeDisplayPng(self.cM));
		boardPng = ImageTk.PhotoImage(boardPng.resize((winS, winS)));
		
		# draw the image
		self.label.config(image=boardPng);
		self.label.image = boardPng;
	
	def toggleEngine(self, btn):
		# find what button we have toggled now
		startText = "Start engine";
		stopText = "Stop engine";
		isStartInnerText = btn["text"] == startText;

		# ENGINE IS ROARING!!!!
		btn.config(image=PhotoImage(), text=(stopText if isStartInnerText else startText));
		print(f"Engine {"starting" if isStartInnerText else "stopping"}");
		self.engineOn = not self.engineOn;

	def readSetFen(self):
		with open("fenRead.txt", "r+") as file:
			self.board.set_fen(file.readline());
		self.reloadBoard();

	# handles the clicking of a piece, this is where moves are made
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
		moveWasMade = False; # for UI delay
		if len(cM) == 4:
			sanCurrM = uciM(cM, self.board);
			
			# if legal we push
			if sanCurrM in self.board.legal_moves:
				self.board.push(sanCurrM);
				moveWasMade = True;
				print("UI move made:", sanCurrM);
    
			cM = "";
		self.cM.set(cM);

		self.reloadBoard(); # reload the board after the move
		if moveWasMade and self.engineOn: # engine
			move = callEngine(self.board);
			if move == None: # termination occurred
				print("Good game");
			elif move in self.board.legal_moves:
				self.board.push(move);
				self.reloadBoard();
			else:
				print("Invalid engine move:", move);

if __name__ == "__main__":    
    # initiliase window
    os.system("cls");
    win = Window();
    win.mainloop();
