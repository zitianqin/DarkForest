import chess
from random import randint

MAX_64BIT = 0xffffffffffffffff;
NUM_COLOURS = 2;
NUM_PIECE_TYPES = 6;
NUM_SQUARES = len(chess.SQUARES);
NUM_FILES = 8;
NUM_CASTLES = 4;

MAX_TABLELEN = 0xffffffff;

ranNums = [];
def ran64():
    newNum = randint(0, MAX_64BIT);
    while newNum in ranNums:
        newNum = randint(~MAX_64BIT, MAX_64BIT);
    ranNums.append(newNum);
    return newNum;    

class Zobrist():
    def __init__(self) -> None:
        self.zPcMap = [[[0] * NUM_SQUARES] * NUM_PIECE_TYPES] * NUM_COLOURS; # pieces, including colour and type
        self.zEnPass = [0] * NUM_FILES; # enpassant rights
        self.zCastle = [0] * NUM_CASTLES; # castle right
        self.zB2M = ran64(); # black to move

        # fill it up, baby
        self.fillArray();
        
        # the transposition table
        self.table = {};
        self.numEntries = 0;
    
    def fillArray(self):
        # pieces
        for i in range(NUM_COLOURS):
            for j in range(NUM_PIECE_TYPES):
                for k in range(NUM_SQUARES):
                    self.zPcMap[i][j][k] = ran64();

        # enpassant
        for i in range(NUM_FILES):
            self.zEnPass[i] = ran64();

        # castling
        for i in range(NUM_CASTLES):
            self.zCastle[i] = ran64();
    
    def getHash(self, board):
        hash = 0;
        
        # pieces
        for sq in chess.SQUARES:
            pc = board.piece_at(sq);
            if pc == None: continue;
            clr = pc.color;
            pType = pc.piece_type - 1;
            
            hash ^= self.zPcMap[clr][pType][sq];
        
        # enpassant
        epSq = board.ep_square;
        if epSq != None:
            hash ^= self.zEnPass[chess.square_file(epSq)];
        
        # castling
        castleBits = board.castling_rights;
        if castleBits & chess.BB_A8:
            hash ^= self.zCastle[0];
        if castleBits & chess.BB_A1:
            hash ^= self.zCastle[1];
        if castleBits & chess.BB_H8:
            hash ^= self.zCastle[2];
        if castleBits & chess.BB_H1:
            hash ^= self.zCastle[3];
        
        # black to move
        if not board.turn:
            hash ^= self.zB2M;

        return hash;
    
    def hasHash(self, hash):
        return hash in self.table;
    
    def getEntry(self, hash):
        return self.table[hash];
    
    # we assume args is an array
    def insertEntry(self, hash, args):
        self.table[hash] = args;
        self.numEntries += 1;

    # clears the tables NOT the mappings
    def clearTable(self):
        self.table = {};
