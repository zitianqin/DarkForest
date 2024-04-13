import pyautogui as pag

# file paths
BUFF_PNG_FILE = "buff.png";

# graphics sizing
winS = int(pag.size()[1] * 2 / 3);
ratS = 0.245;
winClickRat = 1.23; # scaling up viewport to mouse click
sqS = winS * winClickRat / 8;

# colours
WIN_BG_COL = "#abcabc";
SELECT_COL = "#99dd99";
ATTACKING_COL = "#aa4444";
MOVING_COL = "#9999dd";
CHECK_COL = "#cc5555";
CHECKMATE_COL = "#aa1111";
STALEMATE_COL = "#999999";

# standard widget dimensions
NUM_BTNS = 2;
BTN_HEIGHT = 50;
BTN_WIDTH = int(winS / NUM_BTNS);
