import chess
from random import randint

MAX_64BIT = 0xffffffffffffffff;
NUM_SQUARES = len(chess.SQUARES);
NUM_PIECE_TYPES = 12;
MAX_MAPNUMS = NUM_SQUARES * NUM_PIECE_TYPES;

zobristMap = [None] * NUM_SQUARES;

transTable = {};

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
    return hash in list(transTable.keys());

# if there's an entry we return it, otherwise 
def getEntry(hash):
    return transTable[hash];

# adds an entry to the table
def insertEntry(hash, eval):
    # limit the number of entries
    if len(list(transTable.keys())) >= 0xffffff:
        transTable.pop(list(transTable.keys())[0]);
    
    # insert and return
    transTable[hash] = eval;
    obj = {hash: eval};
    return obj;
