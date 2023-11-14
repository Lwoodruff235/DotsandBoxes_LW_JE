# Lauren Woodruff and Jayden Eden
# October 18th, 2023 
# Dots and Boxes

from tkinter import *
import numpy as ny
from db import DAB

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

class DotsAndBoxes:
    def __init__(self):
        self.window = Tk()
        self.window.tittle('Dots n Boxes')
        self.canvas = Canvas(self.window, width = board_size, height = board_size)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.refresh_board()
        self.play_again()
    
    def play_again(self):
        self.refresh_board()
        self.board_status = ny.zeros(shape=(numOfDots - 1, numOfDots-1))
        self.row_status = ny.zeros(shape=(numOfDots, numOfDots - 1))
        self.col_status = ny.zeros(shape=(numOfDots - 1, numOfDots))

        #User input
        self.player1_starts = not self.player1_starts
        self.player1_turn = not self.player1_starts
        self.reset_board = False
        self.turntext_handle = []

        self.already_marked_boxes = []
        self.display_turn_text()

    def main(self):
        self.window.mainloop()
    
# Game Logic 
    def isGridOcc(self, logical_postion, type):
        r = logical_postion[0]
        c = logical_postion[1]
        occ = True

        if type == 'row' and self.row_status[c][r] == 0:
            occ = False
        if type == 'col' and self.col_status[c][r] == 0:
            occ = False
    def convertGridToLogicalPos(self, grid-position):
        grid_position = ny.array(grid_position)
        position = (grid_position - disBetweenDots/4)//(disBetweenDots/2)

        type = False
        logical_position = []
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            r = int((position[0] - 1) // 2)
            c = int(position[1] // 2)
            logical_position = [r, c]
            type = 'row'
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            c = int(position[1] - 1)
            r = int(position[0] // 2)
            logical_position = [r, c]
            type = 'col'
        
        return logical_position, type

    def markBox(self):
        boxes = ny.argwhere(self.board_status == -4)
        for box in boxes:
            if list(box) not in self.already_marked-boxes and list(box) != []:
                self.already_marked_boxes.append(list(box))
                color = p1Fill
                self.shade_box(box, color)

        boxes = ny.argwhere(self.board_status == 4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) != []:
                self.already_marked_boxes.append(list(box))
                color = p2Fill
                self.shade_box(box, color)
    def updateBoard(self, type, logical_position):
        r = logical_position[0]
        c = logical_position[1]
        val = 1
        if self.player1_turn:
            val -= 1
        if c < (numOfDots - 1) and r < (numOfDots - 1):
            self.board_status[c][r] += val
        
        if type == 'row':
            self.row_status[c][r] = 1
            if c >= 1:
                self.board_status[c-1][r] += val
        elif type == 'col':
            self.col_status[c][r] = 1
            if r >= 1:
                self.board_status[c][r-1] += val
                
    def isGameover(self):
        return (self.row_status == 1).all() and (self.col_status == 1).all()






