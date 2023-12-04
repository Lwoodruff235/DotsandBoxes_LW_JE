# Lauren Woodruff and Jayden Eden
# October 18th, 2023 
# Dots and Boxes

from tkinter import *
import numpy as np

boardSize = 600
numOfDots = 6
symbolSize = (boardSize / 3 - boardSize / 8) / 2
symbolThickness = 50
dotColor = '#f000ff' #purple dot
p1Color = '#ffac09' # orange line
p1fill = '#ffac09' # orange box fill
p2Color = '#ff00b4' # pink line 
p2Fill = '#ff00b4' # pink box fill
purple = '#f000ff'# tie color
dotWidth = 0.25 * boardSize / numOfDots
edgeWidth = 0.1 * boardSize / numOfDots
disBetweenDots = boardSize / (numOfDots)

class Dots_and_Boxes():
    # ------------------------------------------------------------------
    # Initialization functions
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title('Dots_and_Boxes')
        self.canvas = Canvas(self.window, width = boardSize, height = boardSize)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.player1_starts = True
        self.refresh_board()
        self.play_again()

    def play_again(self):
        self.refresh_board()
        self.board_status = np.zeros(shape=(numOfDots - 1, numOfDots - 1))
        self.row_status = np.zeros(shape=(numOfDots, numOfDots - 1))
        self.col_status = np.zeros(shape=(numOfDots - 1, numOfDots))

        # Input from user in form of clicks
        self.player1_starts = not self.player1_starts
        self.player1_turn = not self.player1_starts
        self.reset_board = False
        self.turntext_handle = []

        self.already_marked_boxes = []
        self.display_turn_text()

    def mainloop(self):
        self.window.mainloop()

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def is_grid_occupied(self, logical_position, type):
        r = logical_position[0]
        c = logical_position[1]
        occupied = True

        if type == 'row' and self.row_status[c][r] == 0:
            occupied = False
        if type == 'col' and self.col_status[c][r] == 0:
            occupied = False

        return occupied

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        position = (grid_position - disBetweenDots/4) // (disBetweenDots/2)

        type = False
        logical_position = []
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            r = int((position[0]-1)//2)
            c = int(position[1]//2)
            logical_position = [r, c]
            type = 'row'
            # self.row_status[c][r]=1
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            c = int((position[1] - 1) // 2)
            r = int(position[0] // 2)
            logical_position = [r, c]
            type = 'col'

        return logical_position, type

    def mark_box(self):
        boxes = np.argwhere(self.board_status == -4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) !=[]:
                self.already_marked_boxes.append(list(box))
                color = p1fill
                self.shade_box(box, color)

        boxes = np.argwhere(self.board_status == 4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) !=[]:
                self.already_marked_boxes.append(list(box))
                color = p2Fill
                self.shade_box(box, color)

    def update_board(self, type, logical_position):
        r = logical_position[0]
        c = logical_position[1]
        val = 1
        if self.player1_turn:
            val =- 1

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

    def is_gameover(self):
        return (self.row_status == 1).all() and (self.col_status == 1).all()

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def make_edge(self, type, logical_position):
        if type == 'row':
            start_x = disBetweenDots/2 + logical_position[0] * disBetweenDots
            end_x = start_x + disBetweenDots
            start_y = disBetweenDots/2 + logical_position[1] * disBetweenDots
            end_y = start_y
        elif type == 'col':
            start_y = disBetweenDots / 2 + logical_position[1] * disBetweenDots
            end_y = start_y + disBetweenDots
            start_x = disBetweenDots / 2 + logical_position[0] * disBetweenDots
            end_x = start_x

        if self.player1_turn:
            color = p1Color
        else:
            color = p2Color
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=edgeWidth)

    def display_gameover(self):
        player1_score = len(np.argwhere(self.board_status == -4))
        player2_score = len(np.argwhere(self.board_status == 4))

        if player1_score > player2_score:
            # Player 1 wins
            text = 'Winner: Player 1 '
            color = p1Color
        elif player2_score > player1_score:
            text = 'Winner: Player 2 '
            color = p2Color
        else:
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(boardSize / 2, boardSize / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(boardSize / 2, 5 * boardSize / 8, font="cmr 40 bold", fill=purple,
                                text=score_text)

        score_text = 'Player 1 : ' + str(player1_score) + '\n'
        score_text += 'Player 2 : ' + str(player2_score) + '\n'
        # score_text += 'Tie                    : ' + str(self.tie_score)
        self.canvas.create_text( boardSize / 2, 3 * boardSize / 4, font="cmr 30 bold", fill=purple,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(boardSize / 2, 15 * boardSize / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    def refresh_board(self):
        for i in range(numOfDots):
            x = i * disBetweenDots + disBetweenDots/2
            self.canvas.create_line(x, disBetweenDots/2, x,
                                    boardSize - disBetweenDots/2,
                                    fill='gray', dash = (2, 2))
            self.canvas.create_line(disBetweenDots/2, x,
                                    boardSize - disBetweenDots/2, x,
                                    fill='gray', dash=(2, 2))

        for i in range(numOfDots):
            for j in range(numOfDots):
                start_x = i * disBetweenDots + disBetweenDots/2
                end_x = j * disBetweenDots + disBetweenDots/2
                self.canvas.create_oval(start_x - dotWidth / 2, end_x- dotWidth / 2, start_x + dotWidth / 2,
                                        end_x+dotWidth / 2, fill = dotColor,
                                        outline = dotColor)

    def display_turn_text(self):
        text = 'Next turn: '
        if self.player1_turn:
            text += 'Player1'
            color = p1Color
        else:
            text += 'Player2'
            color = p2Color

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(boardSize - 5*len(text),
                                                      boardSize - disBetweenDots/8,
                                                       font="cmr 15 bold", text=text, fill=color)


    def shade_box(self, box, color):
        start_x = disBetweenDots / 2 + box[1] * disBetweenDots + edgeWidth/2
        start_y = disBetweenDots / 2 + box[0] * disBetweenDots + edgeWidth/2
        end_x = start_x + disBetweenDots - edgeWidth
        end_y = start_y + disBetweenDots - edgeWidth
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')

    def display_turn_text(self):
        text = 'Next turn: '
        if self.player1_turn:
            text += 'Player1'
            color = p1Color
        else:
            text += 'Player2'
            color = p2Color

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(boardSize- 5 * len(text),
                                                       boardSize - disBetweenDots/8,
                                                       font="cmr 15 bold",text=text, fill=color)

    def click(self, event):
        if not self.reset_board:
            grid_position = [event.x, event.y]
            logical_positon, valid_input = self.convert_grid_to_logical_position(grid_position)
            if valid_input and not self.is_grid_occupied(logical_positon, valid_input):
                self.update_board(valid_input, logical_positon)
                self.make_edge(valid_input, logical_positon)
                self.mark_box()
                self.refresh_board()
                self.player1_turn = not self.player1_turn

                if self.is_gameover():
                    # self.canvas.delete("all")
                    self.display_gameover()
                else:
                    self.display_turn_text()
        else:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False


dab = Dots_and_Boxes()
dab.mainloop()
