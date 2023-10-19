# Lauren Woodruff and Jayden Eden
# October 18th, 2023 
# Dots and Boxes

from tkinter import *
import numpy as ny
from db import DotsAndBoxes

#----------VARIABLES----------
board_size = 600
numOfDots = 6
symbolSize = (board_size / 3 - board_size / 8) / 2
symbolWidth = 50 
dotColor = '#f000ff' #purple line
p1Color = '#ffac09' # orange 
p1Fill = 'fee131' # orange box fill
p2Color = '#ff00b4' # pink line 
p2Fill = 'ff6ec7' # pink box fill
green = '#0bff01'
dotWidth = 0.25 * board_size/numOfDots
edgeWidth = 0.1 * board_size/numOfDots
disBetweenDots = board_size/numOfDots
