import chess
from random import randint

MAX_64BIT = 0xffffffffffffffff;
NUM_SQUARES = len(chess.SQUARES);
NUM_PIECE_TYPES = 12;
MAX_MAPNUMS = NUM_SQUARES * NUM_PIECE_TYPES;
MAX_TABLELEN = 0xffffffff;

zobristMap = [None] * NUM_SQUARES;

transTable = {};
tableLen = 0;

# generates a new unique number for the mappings
mapNums = []; 
def newUniqueMapNum():
    num = randint(0, MAX_64BIT);
    while num in mapNums:
        num = randint(0, MAX_64BIT);
    mapNums.append(num);
    return num;

# initialises the mapping for all pieces for each square
def initZobristMap():
    for sq in chess.SQUARES:
        zobristMap[sq] = {};
        # for each piece, gen unique number
        for pc in range(NUM_PIECE_TYPES):
            zobristMap[sq][pc] = newUniqueMapNum();

# returns the index on a Zobrist map object for a given piece
def getZobristMapIndex(pc):
    return 2*(pc.piece_type - 1) + (1 if pc.color else 0);

# hashes a given board from the Zobrist map
def zobristHash(board):
    hash = 0;
    for sq in chess.SQUARES:
        pc = board.piece_at(sq);
        if pc == None: continue;
        
        hash ^= zobristMap[sq][getZobristMapIndex(pc)];
    return hash;

# we convert the board to a hash and then see if it's in the table
def hasTableEntry(hash):
    return hash in transTable;

# if there's an entry we return it, otherwise 
def getEntry(hash):
    return transTable[hash];

# adds an entry to the table
def insertEntry(hash, eval):
    global tableLen;
    # limit the number of entries
    if tableLen >= MAX_TABLELEN:
        keys = list(transTable.keys());
        numPop = int(MAX_TABLELEN / 3);
        for i in range(0, numPop):
            transTable.pop(keys[i]);
        tableLen -= numPop;
    
    # insert and return
    transTable[hash] = eval;
    tableLen += 1;

# completely wipes the table
def clearTable():
    global transTable;
    transTable = {};
