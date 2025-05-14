import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys
import pickle
import eval

myfont = ("Arial", 18)

class App:
    def __init__(self, root):
        self.root = root
        self.count = 0
        self.current_index = -1
        self.current_canvas = None
        self.analysis = False
        self.canvases = {}

        root.bind("<Left>", self.switch_left)
        root.bind("<Right>", self.switch_right)
        root.bind("<Up>", self.switch_up)
        root.bind("<Down>", self.switch_down)
        root.focus_set()

    def create_canvas(self, xgid):
        canvas_1 = tk.Canvas(self.root, width=600, height=560, bg="black")
        canvas_2 = tk.Canvas(self.root, width=600, height=560, bg="black")
        self.current_index += 1
        self.canvases[self.current_index] = (canvas_1, canvas_2)
        self.current_canvas = canvas_1
        self.count += 1
        configure_board(canvas_1, Board(xgid))
        configure_board(canvas_2, Board(xgid), analysis=eval.get_stats(xgid))
        print(len(self.canvases))
        print(self.current_index)
        print(self.count)
        print(xgid)

    def show_canvas(self):
        self.current_canvas.pack_forget()
        if self.analysis: self.current_canvas = self.canvases[self.current_index][1]
        else: self.current_canvas = self.canvases[self.current_index][0]
        self.current_canvas.pack()

    def switch_left(self, event):
        print("left")
        if self.analysis == False:
            self.current_index -= 1
            if self.current_index == -1:
                print("back")
                self.current_index = self.count - 1
            self.show_canvas()
            print(len(self.canvases))
            print(self.current_index)
            print(self.count)

    def switch_right(self, event):
        print("right")
        if self.analysis == False:
            self.current_index += 1
            if self.current_index == self.count:
                print("back")
                self.current_index = 0
            self.show_canvas()
            print(len(self.canvases))
            print(self.current_index)
            print(self.count)

    def switch_up(self, event):
        self.analysis = True
        self.show_canvas()

    def switch_down(self, event):
        self.analysis = False
        self.show_canvas()



def get_dice_image(d):
    if d == 1:
        image = Image.open(r'C:\Users\aadam\Documents\2025_Blunderbase\Graphics\Dice_1.png')
    elif d == 2:
        image = Image.open(r'C:\Users\aadam\Documents\2025_Blunderbase\Graphics\Dice_2.png')
    elif d == 3:
        image = Image.open(r'C:\Users\aadam\Documents\2025_Blunderbase\Graphics\Dice_3.png') 
    elif d == 4:
        image = Image.open(r'C:\Users\aadam\Documents\2025_Blunderbase\Graphics\Dice_4.png')
    elif d == 5:
        image = Image.open(r'C:\Users\aadam\Documents\2025_Blunderbase\Graphics\Dice_5.png')
    elif d == 6:
        image = Image.open(r'C:\Users\aadam\Documents\2025_Blunderbase\Graphics\Dice_6.png')
    photo = image.resize((30,30), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(photo)
    return photo

class Board:
    def __init__(self, xgid):
        print("XGID!", xgid)
        parts = xgid.split(':')
        board = parts[0][5:]
        cube = parts[1]
        cube_position = parts[2]
        turn = parts[3]
        dice = parts[4]
        score_bottom = parts[5]
        score_top = parts[6]
        crawford = parts[7]
        length = parts[8]
        max_cube = parts[9]

        home_bot, home_top = 15, 15
        self.board = [0] * 24
        self.top_pip_count, self.bottom_pip_count = 0, 0
        for i, c in enumerate(board[1:-1]):
            if ord(c) == 45:
                self.board[i] = 0
            elif ord(c) < 80:
                self.board[i] = ord(c) - 64
                home_bot -= self.board[i]
                self.bottom_pip_count += ((i+1) * self.board[i])
                print(c, home_top, home_bot)
            else:
                self.board[i] = 96 - ord(c)
                home_top += self.board[i]
                self.top_pip_count += ((24-i) * (-self.board[i]))
                print(c, home_top, home_bot)
        print("BOARD:", board)

        if board[-1] == '-': bottom_bar = 0
        else: 
            bottom_bar = ord(board[-1]) - 64
            home_bot -= bottom_bar
        if board[0] == '-': top_bar = 0
        else:
            top_bar = ord(board[0]) - 96
            home_top -= top_bar
        self.bar = (bottom_bar, top_bar)
        self.home = (home_bot, home_top)
        self.bottom_pip_count += (25 * self.bar[0])
        self.top_pip_count += (25 * self.bar[1])

        if cube == '0': self.cube = '64'
        else: self.cube = str(2**int(cube))
        self.cube_pos = int(cube_position)
        self.dice = (int(dice[0]), int(dice[1]))
        if dice == '00': self.isDouble = True
        else: 
            self.isDouble = False
            self.dice1 = get_dice_image(int(dice[0]))
            self.dice2 = get_dice_image(int(dice[1]))

        self.score_bot = score_bottom
        self.score_top = score_top
        if crawford == '1': self.crawford = True
        else: self.crawford = False

        self.length = length
        print("finished:")

def place_checkers(canvas, pos, num, color):
    checkers = min(5, num)
    if color == 'white': text_color = 'black'
    else: text_color = 'white'
    if pos >= 18:
        for i in range(checkers):
            x = canvas.create_oval(320+40*(pos-18), 40+40*i, 360+40*(pos-18), 80+40*i, fill=color)
            if num > 5:
                canvas.create_text(340+40*(pos-18), 220, text=str(num), fill=text_color)

    elif pos >= 12:
        for i in range(checkers):
            x = canvas.create_oval(40+40*(pos-12), 40+40*i, 80+40*(pos-12), 80+40*i, fill=color)
            if num > 5:
                canvas.create_text(60+40*(pos-12), 220, text=str(num), fill=text_color)
    elif pos >= 6:
        for i in range(checkers):
            canvas.create_oval(240-40*(pos-6), 480-40*i, 280-40*(pos-6), 520-40*i, fill=color)
            if num > 5:
                canvas.create_text(260-40*(pos-6), 340, text=str(num), fill=text_color)
    else:
        for i in range(checkers):
            x = canvas.create_oval(520-40*(pos), 480-40*i, 560-40*(pos), 520-40*i, fill=color)
            if num > 5:
                canvas.create_text(540-40*(pos), 340, text=str(num), fill=text_color)

def create_dice(canvas, boardinfo):
    canvas.dice1=boardinfo.dice1
    canvas.create_image(420, 280, image=boardinfo.dice1)

    canvas.dice2=boardinfo.dice2
    canvas.create_image(460, 280, image=boardinfo.dice2)

def unpack_analysis(lines):
    text = ""
    for line in lines:
        text += (line + '\n')
    return text

def configure_board(canvas, boardinfo, analysis=None):
    canvas.create_rectangle(40, 40, 560, 520, fill='gray')
    canvas.create_rectangle(0, 0, 600, 40, fill='black')
    canvas.create_rectangle(0, 650, 600, 560, fill='black')
    canvas.create_rectangle(0, 40, 40, 520, fill='brown')
    canvas.create_rectangle(560, 40, 600, 520, fill='brown')
    canvas.create_rectangle(280, 40, 320, 520, fill='brown')

    canvas.create_line(300, 40, 300, 520, width=2)

    for i in range(3):
        canvas.create_polygon([40+80*i, 40, 80+80*i, 40, 60+80*i, 240], fill='green')
        canvas.create_polygon([80+80*i, 40, 120+80*i, 40, 100+80*i, 240], fill='lime')

        canvas.create_polygon([320+80*i, 40, 360+80*i, 40, 340+80*i, 240], fill='green')
        canvas.create_polygon([360+80*i, 40, 400+80*i, 40, 380+80*i, 240], fill='lime')

        canvas.create_polygon([40+80*i, 520, 80+80*i, 520, 60+80*i, 320], fill='lime')
        canvas.create_polygon([80+80*i, 520, 120+80*i, 520, 100+80*i, 320], fill='green')
        canvas.create_polygon([320+80*i, 520, 360+80*i, 520, 340+80*i, 320], fill='lime')
        canvas.create_polygon([360+80*i, 520, 400+80*i, 520, 380+80*i, 320], fill='green')

    canvas.create_text(300, 20, text=str(boardinfo.top_pip_count), font=myfont, fill='white')
    canvas.create_text(300, 540, text=str(boardinfo.bottom_pip_count), font=myfont, fill='white')

    for i in range(24):
        checkers = boardinfo.board[i]
        if checkers > 0:
            place_checkers(canvas, i, checkers, 'white')
        elif checkers < 0:
            place_checkers(canvas, i, -checkers, 'black')

    if boardinfo.bar[0] > 0:
        x = canvas.create_oval(280, 160, 320, 200, fill='white')
        if boardinfo.bar[0] > 1:
            canvas.create_text(300, 180, text=str(boardinfo.bar[0]), font=myfont, fill='black')

    if boardinfo.bar[1] > 0:
        x = canvas.create_oval(280, 360, 320, 400, fill='black')
        if boardinfo.bar[1] > 1:
            canvas.create_text(300, 380, text=str(boardinfo.bar[1]), font=myfont, fill='white')

    for i in range(boardinfo.home[0]):
        canvas.create_rectangle(565, 462-8*i, 595, 470-8*i, fill='white', outline='black')
    for i in range(boardinfo.home[1]):
        canvas.create_rectangle(565, 90+8*i, 595, 98+8*i, fill='black', outline='white')

    if boardinfo.cube_pos == 0:
        canvas.create_rectangle(285, 265, 315, 295, fill='white', outline='black')
        canvas.create_text(300, 280, text='64', font=myfont, fill='black')
    elif boardinfo.cube_pos == 1:
        canvas.create_rectangle(5, 480, 35, 510, fill='white', outline='black')
        canvas.create_text(20, 495, text=boardinfo.cube, font=myfont, fill='black')
    else:
        canvas.create_rectangle(5, 50, 35, 80, fill='white', outline='black')
        canvas.create_text(20, 65, text=boardinfo.cube, font=myfont, fill='black')

    canvas.create_text(580, 60, text=boardinfo.score_top + "/" + boardinfo.length, font=myfont, fill='white')
    canvas.create_text(580, 500, text=boardinfo.score_bot + "/" + boardinfo.length, font=myfont, fill='white')

    if boardinfo.isDouble:
        canvas.create_rectangle(380, 265, 430, 295, fill='white')
        canvas.create_text(405, 280, text='Roll Dice')
        canvas.create_rectangle(450, 265, 500, 295, fill='white')
        canvas.create_text(475, 280, text='Double')
    else:
        create_dice(canvas, boardinfo)

    print("Running the analysis ", analysis)
    if analysis:
        canvas.create_rectangle(0, 0, 600, 560, fill='white', stipple="gray75")
        canvas.create_text(300, 280, text=unpack_analysis(analysis), anchor='center')


def main():
    if len(sys.argv) > 1:
        positions = sys.argv[1]
        full_positions = r"\Users\aadam\Documents\2025_Blunderbase\\" + positions
        print("Start")
        root = tk.Tk()
        app = App(root)

        for filename in os.listdir(full_positions):
            print("Filename", filename)
            file_path = os.path.join(full_positions, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f:
                    graph = pickle.load(f)
                xgid = graph.xgid
                app.create_canvas(xgid)

        root.mainloop()

    else:
        print("ERROR: need an argument");

if __name__ == "__main__":
    main()
