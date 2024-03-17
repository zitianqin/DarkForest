import pyautogui as pag

BUFF_PNG_FILE = "buff.png";
winS = int(pag.size()[1] * 2 / 3);
ratS = 0.245;
winClickRat = 1.23; # scaling up viewport to mouse click
sqS = winS * winClickRat / 8;
currM = ""; # stores current user move sequence

# colours
SELECT_COL = "#99dd99";
ATTACKING_COL = "#aa4444";
MOVING_COL = "#9999dd";
CHECK_COL = "#cc5555";
CHECKMATE_COL = "#aa1111";
STALEMATE_COL = "#333333";
