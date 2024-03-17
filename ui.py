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

# picture displayed
class Board(chess.Board):
    def __init__(self):
        super().__init__();
    
    def writeDisplayPng(self):
        # square that is selected to move next
        slctM = currM[:2];
        slctSq = None if slctM == "" else chess.parse_square(slctM);
        
        # bulk of the colouring
        selected = [];
        attacking = [];
        moving = [];

        # checks for selected piece and that the square isn't empty
        if slctM != "" and self.piece_at(slctSq) != None:
            # convert the square name to the index in chess library
            selected.append(slctSq);
            
            # colour the legal moves
            for move in self.legal_moves:
                # uci expression for the legal move
                uciLegM = self.uci(move);
                
                # check if user selected move is in the legal move
                if slctM in uciLegM:
                    atkSq = chess.parse_square(uciLegM[2:4]);
                    atkPc = self.piece_at(atkSq);
                    currPc = self.piece_at(slctSq);
                    
                    # check if atacking
                    if atkPc != None and not isOnSameTeam(atkPc, currPc):
                        attacking.append(atkSq);
                    else:
                        moving.append(atkSq);
        selectedMapping = dict.fromkeys(selected, SELECT_COL);
        attackingMapping = dict.fromkeys(attacking, ATTACKING_COL);
        movingMapping = dict.fromkeys(moving, MOVING_COL);
        
        # for any checkmates
        checkedKing = [];
        if self.is_checkmate():
            # find king that is checked
            lostKing = "k" if self.outcome().winner else "K";
            for square in chess.SQUARES:
                if str(self.piece_at(square)) == lostKing:
                    checkedKing.append(square);
        checkedKingMapping = dict.fromkeys(checkedKing, CHECKMATE_COL);

        # combine all mappings
        totalMapping = {};
        for mapping in [selectedMapping, attackingMapping, movingMapping, checkedKingMapping]:
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
        
        # construct the label
        self.label = Label(self);
        self.label.pack();
        self.label.bind("<Button>", lambda event: self.handleClick(event));
        
        # construct abstract board
        self.board = Board();
        self.reloadBoard();
        
    def reloadBoard(self):
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
        sqMOff = sqS - offset; # square side length without offset
        pixX = event.x - offset; # calculate w/out the offset
        pixY = event.y - offset;
        indX = floor(pixX / sqMOff); # calculate the indices of square
        indY = 8 - floor(pixY / sqMOff);

        # check for invalid moves
        if isOutOfBounds(indX + 1) or isOutOfBounds(indY):
            currM = "";
            return;
        
        # now we append to user move
        sqPos = chr(indX + ord("a")) + str(indY);
        if sqPos == currM: # also check for null move
            currM = "";
            self.reloadBoard();
            return;
        currM += sqPos;
        
        # check if move was made
        if len(currM) == 4:
            sanCurrM = uciM(currM, self.board);
            
            # if legal we push
            if sanCurrM in self.board.legal_moves:
                self.board.push(sanCurrM);            
            currM = "";
        self.reloadBoard();

if __name__ == "__main__":
    # initialise
    win = Window();
    
    win.mainloop();
    os.remove(BUFF_PNG_FILE); # remove and fluffy files
    sys.exit(1); # Exits shellscript loop
