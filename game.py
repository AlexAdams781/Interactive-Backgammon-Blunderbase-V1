import tkinter as tk
import random as r
import numpy as np
from copy import deepcopy
from PIL import Image, ImageTk


# dictionaries to aid with different names for colors
colorToNum = {
    'white' : 0,
    'black' : 1
}
colorToSymbol = {
    0 : 'O',
    1 : 'X'
}


# the board class has position attributes
class Board:
    def __init__(self):
        self.positions = np.zeros((2, 26))
        self.positions[0][24], self.positions[1][1] = 2, -2
        self.positions[0][19], self.positions[1][6] = -5, 5
        self.positions[0][17], self.positions[1][8] = -3, 3
        self.positions[0][13], self.positions[1][12] = 5, -5
        self.positions[0][12], self.positions[1][13] = -5, 5
        self.positions[0][8], self.positions[1][17] = 3, -3
        self.positions[0][6], self.positions[1][19] = 5, -5
        self.positions[0][1], self.positions[1][24] = -2, 2
        self.maxChecker = [24, 24]

        self.bar = [0, 0]

        self.offBar = (False, False)

        self.launch = [set([24, 13, 8, 6]), set([24, 13, 8, 6])]

        self.positions_copy = deepcopy(self.positions)

    # returns the position of the furthest behind checker
    def newMaxChecker(self, old):
        print('high', self.positions_copy)
        for i in range(old, 0, -1):
            print(i)
            if self.positions_copy[i] > 0:
                return i
        return 0

    # returns all possible legal moves for a player (wrapper)
    def isMove(self, d1, d2, color):
        # recurive function that does the same
        def getAllMovesRec(movesLaunches, dice, bar, maxChecker):
            print(movesLaunches, dice, bar, maxChecker)
            if len(dice) == 0:
                return movesLaunches
            
            if maxChecker <= 6:
                threshold = 0
            else:
                threshold = 1

            d = dice.pop()
            new_movesLaunches = []
            for ml in movesLaunches:
                moves = ml[0]
                launch = ml[1]
                position = ml[2]
                if bar > 0:
                    _launch = set([25])
                else:
                    _launch = launch
                move_count = 0
                for p in _launch:
                    #print('launch', launch, p)
                    launch_copy = deepcopy(launch)
                    moves_copy = deepcopy(moves)
                    self.positions_copy = deepcopy(position)
                    if (p == maxChecker and ((p - d) < threshold)) or (self.positions_copy[p - d] >= -1 and ((p - d) >= threshold)):
                        move_count += 1
                        if p - d > 0:
                            launch_copy.add(p - d)
                            self.positions_copy[p - d] += 1
                        moves_copy.append((p, max(p - d, 0)))
                        self.positions_copy[p] -= 1
                        if self.positions_copy[p] <= 0 and p != 25:
                            launch_copy.remove(p)
                        if p == 25:
                            bar -= 1
                        maxChecker = self.newMaxChecker(maxChecker)
                        new_movesLaunches.append((moves_copy, launch_copy, self.positions_copy))
                if move_count == 0:
                    new_movesLaunches.append(ml)
        
            return getAllMovesRec(new_movesLaunches, dice, bar, maxChecker)
        
        if color == 0:
            launch = self.launch[0]
            position = self.positions[color]
        else:
            launch = self.launch[1]
            position = self.positions[color]
        
        def f(tup):
            a, b, c = tup
            return a

        if d1 != d2:
            allMoves = getAllMovesRec([([], launch, position)], [d1, d2], self.bar[color], self.maxChecker[color])
            allMoves.extend(getAllMovesRec([([], launch, position)], [d2, d1], self.bar[color], self.maxChecker[color]))
            movesLaunches = list(map(f, allMoves))
        else:
            allMoves = getAllMovesRec([([], launch, position)], [d1, d1, d1, d1], self.bar[color], self.maxChecker[color])
            movesLaunches = list(map(f, allMoves))

        maxMoves = 0
        for moves in movesLaunches:
            if len(moves) > maxMoves:
                maxMoves = len(moves)
        print(allMoves)
        return maxMoves


    # changes the board positions based on a single regular move
    def moveOneBoard(self, pre, post, player):
        print('signal')
        if self.positions[player][post] == -1:
            self.positions[player][post] = 1
            self.positions[(player+1)%2][25-post] = -1
            if player == 0:
                self.Blaunch.remove(25 - post)
            else:
                self.Wlaunch.remove(25 - post)
            self.bar[(player+1)%2] += 1
            
            self.maxChecker[(player+1)%2] = 25
        else:
            self.positions[player][post] += 1
            self.positions[(player+1)%2][25 - post] -= 1
        self.positions[player][pre] -= 1
        self.positions[(player+1)%2][25 - pre] += 1

        self.maxChecker[player] = self.newMaxChecker(player, self.maxChecker[player])
        if player == 0:
            if post > 0:
                self.Wlaunch.add(post)
            if self.positions[0][pre] == 0:
                self.Wlaunch.remove(pre)
        else:
            if post > 0:
                self.Blaunch.add(post)
            if self.positions[1][pre] == 0:
                self.Blaunch.remove(pre)
   
   # changes the board positions based on a single move from the bar
    def moveOneBar(self, post, player):
        if self.positions[player][post] == -1:
            self.positions[player][post] = 1
            self.positions[(player+1)%2][25-post] = -1
            if player == 0:
                self.Blaunch.remove(25 - post)
            else:
                self.Wlaunch.remove(25 - post)
            self.bar[(player+1)%2] += 1

            self.maxChecker[(player+1)%2] = 25
        else:
            self.positions[player][post] += 1
            self.positions[(player+1)%2][25-post] -= 1

        self.bar[player] -= 1
        self.maxChecker[player] = self.newMaxChecker(player, self.maxChecker[player])
        if player == 0:
            self.Wlaunch.add(post)
        else:
            self.Blaunch.add(post)

    # changes the board positions based on a single move to home
    def move(self, player, moveSet, mode):
        if moveSet != 'pass':
            if mode == 'pvp':
                for m in moveSet:
                    [m11, m12] = [x for x in m.split('/')]
                    if m11 == 'bar':
                        self.moveOneBar(int(m12), colorToNum[player])
                    elif m12 == 'off':
                        self.moveOneBoard(int(m11), 0, colorToNum[player])
                    else:
                        self.moveOneBoard(int(m11), int(m12), colorToNum[player])
            else:
                for m in moveSet:
                    print('move:', m)
                    m1, m2 = m
                    if m1 == 25:
                        self.moveOneBar(m2, colorToNum[player])
                    elif m2 <= 0:
                        self.moveOneBoard(m1, 0, colorToNum[player])
                    else:
                        self.moveOneBoard(m1, m2, colorToNum[player])

    # checks if anyone won the game
    def winCondition(self):
        if self.positions[0][0] == 15:
                print('White wins!')
                return True
        if self.positions[1][0] == 15:
                print('Black wins!')
                return True
        return False


class tkinterApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (startPage, mainPage):
            frame  = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.show_frame(startPage)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class startPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.columnconfigure(1, weight=1)
        self.controller = controller
        self.bind("<Button-1>", self.on_click)

        welcome_lbl = tk.Label(self, text='Welcome to Backgammon! \n Press anywhere to start')
        welcome_lbl.place(relx=0.5, rely=0.5, anchor='center')

    def on_click(self, A):
        self.controller.show_frame(mainPage)


class firstPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        canvas = tk.Canvas(self)

        canvas.create_rectangle()
        


class mainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.swap = False
        self.image_white_checker = Image.open(r'C:\Users\aadam\Documents\Academic\CMU\Spring 2023\Algorithm Design and Analysis\Code\images\white_checker.png').convert('RGBA')
        self.photo_white_checker = ImageTk.PhotoImage(self.image_white_checker)
        self.moves = []
        self.d = []
        self.dice_position = 0
        self.board = Board()
        self.board_copy = deepcopy(self.board)
        self.turn = 'white'
        self.final_pip_count = [167, 167]

        #self.image_black_checker = Image.open(r'C:\Users\aadam\Documents\Academic\CMU\Spring 2023\Algorithm Design and Analysis\Code\images\black_checker.png')
        #self.photo_black_checker = self.image_black_checker.resize((50,50), Image.Resampling.LANCZOS)
        #self.photo_black_checker = ImageTk.PhotoImage(self.photo_black_checker).convert('RGBA')
        self.configureBoard(True)
        

    def firstRoll_fn(self):
        self.canvas.delete(self.firstRollSign)
        self.canvas.delete(self.firstRoll_lbl)
        self.firstRoll_btn.destroy()

        self.roll_fn()
        

    def roll_fn(self):
        self.d1, self.d2 = r.randint(1, 6), r.randint(1, 6)
        if self.d1 == self.d2:
            self.d = [self.d1, self.d1, self.d1, self.d1]
        else:
            self.d = [self.d1, self.d2]
        self.dice_limit = self.board.isMove(self.d1, self.d2, colorToNum[self.turn])
        self.isDice = True
        self.create_dice(self.d1, self.d2)
        self.configureBoard(False)


    def placeCheckers(self, pos, num, color):
        checkers = min(5, num)
        if color == 'white':
            text_color = 'black'
            self.pip_count[colorToNum[color]] += pos*max(num, 0)
        else:
            text_color = 'white'
            self.pip_count[colorToNum[color]] += (25-pos)*max(0, num)
        if pos > 18:
            for i in range(checkers):
                x = self.canvas.create_oval(400+50*(pos-19), 50+50*i, 450+50*(pos-19), 100+50*i, fill=color)
                if num > 5:
                    self.canvas.create_text(425+50*(pos-19), 275, text=str(num), fill=text_color)
                self.canvas.tag_bind(x, "<Button-1>", lambda k: self.move_fn(pos, color))
                
        elif pos > 12:
            for i in range(checkers):
                x = self.canvas.create_oval(50+50*(pos-13), 50+50*i, 100+50*(pos-13), 100+50*i, fill=color)
                if num > 5:
                    self.canvas.create_text(75+50*(pos-13), 275, text=str(num), fill=text_color)
                self.canvas.tag_bind(x, "<Button-1>", lambda k: self.move_fn(pos, color))
        elif pos > 6:
            for i in range(checkers):
                x = self.canvas.create_oval(300-50*(pos-7), 600-50*i, 350-50*(pos-7), 650-50*i, fill=color)
                if num > 5:
                    self.canvas.create_text(325-50*(pos-7), 425, text=str(num), fill=text_color)
                self.canvas.tag_bind(x, "<Button-1>", lambda k: self.move_fn(pos, color))
        else:
            for i in range(checkers):
                x = self.canvas.create_oval(650-50*(pos-1), 600-50*i, 700-50*(pos-1), 650-50*i, fill=color)
                if num > 5:
                    self.canvas.create_text(675-50*(pos-1), 425, text=str(num), fill=text_color)
                self.canvas.tag_bind(x, "<Button-1>", lambda k: self.move_fn(pos, color))


    def configureBoard(self, isStart):
        self.canvas = tk.Canvas(self, width=750, height=700)
        self.canvas.place(x=0, y=0)

        self.canvas.create_rectangle(50, 50, 700, 650, fill='gray')
        self.canvas.create_rectangle(0, 0, 750, 50, fill='black')
        self.canvas.create_rectangle(0, 650, 750, 700, fill='black')
        self.canvas.create_rectangle(0, 50, 50, 650, fill='brown')
        self.canvas.create_rectangle(700, 50, 750, 650, fill='brown')
        self.canvas.create_rectangle(350, 50, 400, 650, fill='brown')

        self.canvas.create_line(375, 50, 375, 650, width=2)

        self.pip_count = [0, 0]

        for i in range(3):
            self.canvas.create_polygon([50+100*i, 50, 100+100*i, 50, 75+100*i, 300], fill='green')
            self.canvas.create_polygon([100+100*i, 50, 150+100*i, 50, 125+100*i, 300], fill='lime')

            self.canvas.create_polygon([400+100*i, 50, 450+100*i, 50, 425+100*i, 300], fill='green')
            self.canvas.create_polygon([450+100*i, 50, 500+100*i, 50, 475+100*i, 300], fill='lime')

            self.canvas.create_polygon([50+100*i, 650, 100+100*i, 650, 75+100*i, 400], fill='lime')
            self.canvas.create_polygon([100+100*i, 650, 150+100*i, 650, 125+100*i, 400], fill='green')

            self.canvas.create_polygon([400+100*i, 650, 450+100*i, 650, 425+100*i, 400], fill='lime')
            self.canvas.create_polygon([450+100*i, 650, 500+100*i, 650, 475+100*i, 400], fill='green')

        self.canvas.create_text(375, 25, text='WHITE', fill='white')
        self.canvas.create_text(375, 675, text='BLACK', fill='white')

        self.board.launch = [set(), set()]
        self.board.maxChecker = [0, 0]
        self.found_max_black = False

        for i in range(1, 25):
            checkers = int(self.board.positions[0][i])
            if checkers > 0:
                self.placeCheckers(i, checkers, 'white')
                self.board.launch[0].add(i)
                self.board.maxChecker[0] = i
            elif checkers < 0:
                self.placeCheckers(i, -checkers, 'black')
                self.board.launch[1].add(25-i)
                if not self.found_max_black:
                    self.board.maxChecker[1] = 25-i
                    self.found_max_black = True

        if self.board.bar[0] > 0:
            x = self.canvas.create_oval(350, 200, 400, 250, fill='white')
            if self.board.bar[0] > 1:
                self.canvas.create_text(375, 225, text=str(self.board.bar[0]))
            self.canvas.tag_bind(x, "<Button-1>", lambda k: self.move_fn(25, 'white'))
        self.pip_count[0] += 25*self.board.bar[0]

        if self.board.bar[1] > 0:
            x = self.canvas.create_oval(350, 450, 400, 500, fill='black')
            if self.board.bar[1] > 1:
                self.canvas.create_text(375, 475, text=str(self.board.bar[1]), fill='white')
            self.canvas.tag_bind(x, "<Button-1>", lambda k: self.move_fn(0, 'black'))
        self.pip_count[1] += 25*self.board.bar[1]

        self.canvas.create_text(375, 75, text=str(self.final_pip_count[0]), fill='white')
        self.canvas.create_text(375, 625, text=str(self.final_pip_count[1]), fill='white')

        for i in range(int(self.board.positions[0][0])):
            self.canvas.create_rectangle(705, 580-10*i, 745, 590-10*i, fill='white')
        for i in range(-int(self.board.positions[0][25])):
            self.canvas.create_rectangle(705, 110+10*i, 745, 120+10*i, fill='black', outline='white')

        if isStart:
            self.firstRollSign = self.canvas.create_rectangle(225, 250, 525, 450, fill='white')
            self.firstRoll_lbl = self.canvas.create_text(375, 320, text='Roll dice to see who goes first.')
            self.firstRoll_btn = tk.Button(self, height=2, width=10, bg='gray', text='Roll!', command=self.firstRoll_fn)
            self.firstRoll_btn.place(x=375, y=375, anchor='center')
        else:
            self.dice1_btn = tk.Button(self, bg='white', command=self.swap_fn, image=self.photo_d1)
            self.dice1_btn.place(x=510, y=335, height=30, width=30)
            self.dice2_btn = tk.Button(self, bg='white', command=self.swap_fn, image=self.photo_d2)
            self.dice2_btn.place(x=560, y=335, height=30, width=30)
            if self.dice_position > 0:
                self.undo_btn = tk.Button(self, bg='white', text='Undo', command=self.undo_fn)
                self.undo_btn.place(x=90, y=330, height=40, width=100)
            if self.dice_position == self.dice_limit:
                self.done_btn = tk.Button(self, bg='white', text='Done', command=self.done_fn)
                self.done_btn.place(x=210, y=330, height=40, width=100)

    
    def create_dice(self, d1, d2):
        if d1 == 1:
            self.image_d1 = Image.open(r'C:\Users\aadam\Documents\Academic\CMU\Spring 2023\Algorithm Design and Analysis\Code\images\Dice_1.jpg')
        elif d1 == 2:
            self.image_d1 = Image.open(r'C:\Users\aadam\Documents\Academic\CMU\Spring 2023\Algorithm Design and Analysis\Code\images\Dice_2.jpg')
        elif d1 == 3:
            self.image_d1 = Image.open(r'C:\Users\aadam\Documents\Academic\CMU\Spring 2023\Algorithm Design and Analysis\Code\images\Dice_3.jpg')
        elif d1 == 4:
            self.image_d1 = Image.open(r'C:\Users\aadam\Documents\Academic\CMU\Spring 2023\Algorithm Design and Analysis\Code\images\Dice_4.jpg')
        elif d1 == 5:
            self.image_d1 = Image.open(r'C:\Users\aadam\Documents\Academic\CMU\Spring 2023\Algorithm Design and Analysis\Code\images\Dice_5.jpg')
        elif d1 == 6:
            self.image_d1 = Image.open(r'C:\Users\aadam\Documents\Academic\CMU\Spring 2023\Algorithm Design and Analysis\Code\images\Dice_6.jpg')
        self.photo_d1 = self.image_d1.resize((30,30), Image.Resampling.LANCZOS)
        self.photo_d1 = ImageTk.PhotoImage(self.photo_d1)
        self.dice1_btn = tk.Button(self, bg='white', command=self.swap_fn, image=self.photo_d1)
        self.dice1_btn.place(x=510, y=335, height=30, width=30)

        if d2 == 1:
            self.image_d2 = Image.open(r'C:\Users\aadam\Documents\Academic\CMU\Spring 2023\Algorithm Design and Analysis\Code\images\Dice_1.jpg')
        elif d2 == 2:
            self.image_d2 = Image.open(r'C:\Users\aadam\Documents\Academic\CMU\Spring 2023\Algorithm Design and Analysis\Code\images\Dice_2.jpg')
        elif d2 == 3:
            self.image_d2 = Image.open(r'C:\Users\aadam\Documents\Academic\CMU\Spring 2023\Algorithm Design and Analysis\Code\images\Dice_3.jpg')
        elif d2 == 4:
            self.image_d2 = Image.open(r'C:\Users\aadam\Documents\Academic\CMU\Spring 2023\Algorithm Design and Analysis\Code\images\Dice_4.jpg')
        elif d2 == 5:
            self.image_d2 = Image.open(r'C:\Users\aadam\Documents\Academic\CMU\Spring 2023\Algorithm Design and Analysis\Code\images\Dice_5.jpg')
        elif d2 == 6:
            self.image_d2 = Image.open(r'C:\Users\aadam\Documents\Academic\CMU\Spring 2023\Algorithm Design and Analysis\Code\images\Dice_6.jpg')
        self.photo_d2 = self.image_d2.resize((30,30), Image.Resampling.LANCZOS)
        self.photo_d2 = ImageTk.PhotoImage(self.photo_d2)
        self.dice2_btn = tk.Button(self, bg='white', command=self.swap_fn, image=self.photo_d2)
        self.dice2_btn.place(x=560, y=335, height=30, width=30)


    def swap_fn(self):
        if self.dice_position == 0:
            self.d.reverse()
            tmp = self.photo_d1
            self.photo_d1 = self.photo_d2
            self.photo_d2 = tmp
            self.dice1_btn.configure(image=self.photo_d1)
            self.dice2_btn.configure(image=self.photo_d2)

    
    def move_fn(self, pre, color):
        print(self.board.maxChecker)
        if color == self.turn and self.dice_position < self.dice_limit:
            curr_d = self.d[self.dice_position]
            if color == 'black':
                pre = 25 - pre
            post = pre - curr_d
            ind_post = max(post, 0)
            player = colorToNum[color]

            if self.board.positions[player][ind_post] < -1 or (self.board.bar[player] > 0 and pre != 25) or \
                (self.board.maxChecker[player] > 6 and post <= 0) or (pre < self.board.maxChecker[player] and post < 0):
                return
            
            if  self.board.positions[player][ind_post] == -1:
                self.board.positions[player][ind_post] = 1
                self.board.positions[(player+1)%2][25-ind_post] = -1
                self.board.bar[(player+1)%2] += 1
            else:
                self.board.positions[player][ind_post] += 1
                self.board.positions[(player+1)%2][25-ind_post] -= 1

            if pre == 25:
                self.board.bar[player] -= 1
            else:
                self.board.positions[player][pre] -= 1
                self.board.positions[(player+1)%2][25 - pre] += 1

            self.dice_position += 1
            self.configureBoard(False)


    def done_fn(self):
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'

        self.dice_position = 0
        self.final_pip_count = self.pip_count
        self.configureBoard(False)
        self.roll_fn()
        self.board_copy = deepcopy(self.board)


    def undo_fn(self):
        self.board = self.board_copy
        self.board_copy = deepcopy(self.board_copy)
        self.swap = False
        self.dice_position = 0

        self.configureBoard(False)

        

app = tkinterApp()
app.geometry('750x700')
app.mainloop()
