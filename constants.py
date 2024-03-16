import pyautogui as pag

BUFF_PNG_FILE = "buff.png";
winS = int(pag.size()[1] * 2 / 3);
ratS = 0.245;
winClickRat = 1.23; # scaling up viewport to mouse click
sqS = winS * winClickRat / 8;
currM = ""; # stores current user move sequence
