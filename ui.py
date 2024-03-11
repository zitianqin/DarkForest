import chess
import chess.svg

board = chess.Board();
with open("test1.svg", "w+") as file:
    file.write(chess.svg.board(board));
# I guess with this we can just open the new "test1.svg" file every game state
