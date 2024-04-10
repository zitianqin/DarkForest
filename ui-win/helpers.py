import chess
from constants import *

# converts move sequence to SAN representation
def uciM(move, board):
	# check for promotions
	slctPc = board.piece_at(chess.parse_square(move[:2]));
	# must be white in rank 7, black in rank 2, and pawn
	if (
			(isWhite(slctPc) and move[1] == "7") or
			(isBlack(slctPc) and move[1] == "2")
		) and (slctPc.piece_type == chess.PAWN):
		move += "q";
	nextM = chess.Move.from_uci(move);
	return nextM;

# checks for clicking outside of bounds
def isOutOfBounds(index):
	return not (1 <= index and index <= 8);

# checks for white piece
def isWhite(piece):
	if piece == None:
		return False;
	ch = ord(str(piece));
		
	return ord("A") <= ch and ch <= ord("Z");

# checks for black piece
def isBlack(piece):
	if piece == None:
		return False;
	ch = ord(str(piece));
		
	return ord("a") <= ch and ch <= ord("z");

# checks if two pieces are on the same team
def isOnSameTeam(p1, p2):
	return (isWhite(p1) and isWhite(p2)) or (isBlack(p1) and isBlack(p2));

# calculating the selected move and square
def calcSelected(cM):
	slctM = cM.get()[:2];
	slctSq = None if slctM == "" else chess.parse_square(slctM);
	return slctM, slctSq;

# checks which colour is moving from the move stack
def colourFromMove(board):
	lastM = board.peek();
	lastMovedSq = lastM.to_square;
	return not board.color_at(lastMovedSq);

# colours the selected piece square
def selectMap(board, cM):
	slctM, slctSq = calcSelected(cM);
	selected = [];

	# checks for selected piece and that the square isn't empty
	if slctM != "" and board.piece_at(slctSq) != None:
		selected.append(slctSq);
		
	# print(dict.fromkeys(selected, SELECT_COL));
	return dict.fromkeys(selected, SELECT_COL);

# colours the attacking or moveable(legal) squares
def attackMoveMap(board, cM):
	slctM, slctSq = calcSelected(cM);
	attacking = [];
	moving = [];
		
	# checks for selected piece and that the square isn't empty
	if slctM != "" and board.piece_at(slctSq) != None:
		# colour the legal moves
		for move in board.legal_moves:
			# uci expression for the legal move
			uciLegM = board.uci(move);
			
			if slctM in uciLegM:
				atkSq = chess.parse_square(uciLegM[2:4]);
				atkPc = board.piece_at(atkSq);
				currPc = board.piece_at(slctSq);
				
				# check if atacking
				if atkPc != None and not isOnSameTeam(atkPc, currPc):
					attacking.append(atkSq);
				else:
					moving.append(atkSq);
	return dict.fromkeys(attacking, ATTACKING_COL), dict.fromkeys(moving, MOVING_COL);

# colours the checks if any
def checkMap(board):
	checkedKing = [];
	if board.is_check():
		# find king that is checked
		checkedKing.append(board.king(colourFromMove(board)));
	return dict.fromkeys(checkedKing, CHECK_COL);
		
# colours the checkmate if any
def checkmateMap(board):
	checkedMated = [];
	if board.is_checkmate():
		# find king that is checked mated
		checkedMated.append(board.king(colourFromMove(board)));
	return dict.fromkeys(checkedMated, CHECKMATE_COL);

# colours the stalemate if any
def stalemateMap(board):
	staledMated = [];
	if board.is_stalemate() or board.is_insufficient_material():
		# we colour both kings in a stalemate
		for king in [board.king(chess.WHITE), board.king(chess.BLACK)]:
			staledMated.append(king);
	return dict.fromkeys(staledMated, STALEMATE_COL);
