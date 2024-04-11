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

# interfacing with file watching
from concurrent.futures import ThreadPoolExecutor
import watchdog
import watchdog.events
import watchdog.observers

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
	def loadEngineFen(self, win, fen):
		try:
			self.set_fen(fen);
		except Exception as e:
			print("Error: ", e);
		win.reloadBoard();
 
	# when engine writes move to buff file, board pushes move
	def loadEngineMove(self, win, moveStr):
		try:
			move = chess.Move.from_uci(moveStr); # convert output to move
			if move in self.legal_moves:
				self.push(move);
			else:
				print("Invalid engine move");
		except Exception as e:
			print("Error: ", e);
		win.reloadBoard();
	
	# after each move the FEN state and move will be uploaded to their files
	def saveUiMove(self):
		with open(UI_MOVE_OUT, "w+") as file:
			file.write(str(self.peek()));
		with open(UI_FEN_OUT, "w+") as file:
			file.write(str(self.fen()));

# watches events on engine output files
class EngineHandler(watchdog.events.LoggingEventHandler):
    def __init__(self, win):
        super().__init__();
        self.winRef = win;

    # change the on_modified() method to log
    def on_modified(self, event):
        # find which file was modified
        isFenFile = event.src_path == ENGINE_FEN_OUT;
        path = ENGINE_FEN_OUT if isFenFile else ENGINE_MOVE_OUT;

		# open the file to read output
        with open(path, "r") as file:
            global output;
            output = file.readline();
        
        # reading files modifies them with output = ""
        if (output == ""):
            return;
        
        # do the engine output
        if isFenFile:
            self.winRef.board.loadEngineFen(self.winRef, output);
        else:
            self.winRef.board.loadEngineMove(self.winRef, output);

# watcher for engine output
class Watcher(watchdog.observers.Observer):
    def __init__(self, win):
        super().__init__();
        self.handler = EngineHandler(win);
        self.schedule(self.handler, ENGINE_OUT_DIR);
    
    def startWatch(self):
        self.start();
        while self.is_alive():
            self.join(1); # every second we check for engine output
    
    def stopWatch(self):
        self.stop();
        self.join();

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
  
		# construct watcher and threads
		self.watcher = Watcher(self);
		self.watcherTPool = ThreadPoolExecutor(max_workers=2);

		# construct abstract board
		self.board = Board();
		self.reloadBoard();

		# construct button frame
		self.btns = Frame(self, width=winS, height=BTN_HEIGHT);
		self.btns.pack();

		# construct board reset button
		self.resetBoardBtn = SpecBtn(self.btns, "Reset", lambda event: self.board.resetWrapper(self));

		# construct buttons that toggles calls from engine's FEN output
		self.engineBtn = SpecBtn(self.btns, "Start engine watch", lambda event: self.toggleWatchWrap(self.engineBtn));

	def toggleWatchWrap(self, btn):
		# find what button we have toggled now
		startText = "Start engine watch";
		stopText = "Stop engine watch";
		isStartInnerText = btn["text"] == startText;

		# run the command and swap to the other
		if isStartInnerText:
			self.startWatchWrap();
			btn.config(image=PhotoImage(), text=stopText);
		else:
			self.stopWatchWrap();
			btn.config(image=PhotoImage(), text=startText);

	def startWatchWrap(self):
		watcher = self.watcher;
		if watcher.is_alive():
			print("already watching");
		else:
			print("starting watchdog");
			self.watcherTPool.submit(watcher.startWatch);

	def stopWatchWrap(self):
		watcher = self.watcher;
		if not watcher.is_alive():
			print("already stopped");
		else:
			print("stopping watchdog");
			self.watcherTPool.submit(watcher.stopWatch);
			self.watcher = Watcher(self.board); # instance a new watcher for next time

	def reloadBoard(self):
		# grabbing the display
		self.board.writeDisplayPng(self.cM);
		
		# convert and resizing to viewport
		boardPng = Image.open(BUFF_PNG_FILE);
		boardPng = ImageTk.PhotoImage(boardPng.resize((winS, winS)));
		
		# draw the image
		self.label.config(image=boardPng);
		self.label.image = boardPng;
			
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
		if len(cM) == 4:
			sanCurrM = uciM(cM, self.board);
			
			# if legal we push
			if sanCurrM in self.board.legal_moves:
				self.board.push(sanCurrM);
				self.board.saveUiMove();
			cM = "";
		self.cM.set(cM);
		self.reloadBoard();

if __name__ == "__main__":
	# initialise window
	win = Window();
	win.mainloop();

	win.stopWatchWrap(); # make sure to stop watchdog 
	os.remove(BUFF_PNG_FILE); # remove any fluffy files
