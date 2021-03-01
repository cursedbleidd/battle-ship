from tkinter import *
from tkinter import messagebox


class Game(Tk):
    @staticmethod
    def new_game():
        global num_ships, selected_cells
        num_ships = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
        frm_user_field.pack(side=LEFT)
        for y in range(10):
            for x in range(10):
                Cell(pos=(x, y), master=frm_user_field, width=40, height=40, bg='#fff', relief=GROOVE, borderwidth=1)\
                    .grid(row=y, column=x)
        btn_check.pack(side=LEFT)


class Cell(LabelFrame):
    def __init__(self, pos, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.pos = pos
        self.status = 0
        self.bind('<Button-1>', self.select)

    def select(self, event):
        global selected_cells
        if self.status == 1:
            self['bg'] = '#fff'
            self.status = 0
            selected_cells.remove(self)
        elif self.status == 0:
            self['bg'] = '#000'
            self.status = 1
            selected_cells.append(self)

    def unselect(self):
        selected_cells.remove(self)
        print(len(selected_cells))
        self['bg'] = '#fff'
        self.status = 0


class Ship:
    def __init__(self, selected_cells):
        self.cells = selected_cells


def place():
    global selected_cells, num_ships, ships
    if num_ships[0] == len(selected_cells):
        ships.append(Ship(selected_cells))
        num_ships.pop(0)
        selected_cells.clear()
    elif num_ships[0] > len(selected_cells):
        messagebox.showerror('Error', 'Select more cells')
        for cell in selected_cells.copy():
            cell.unselect()
    else:
        messagebox.showerror('Error', 'Too many selected cells')
        for cell in selected_cells.copy():
            cell.unselect()


num_ships = []
selected_cells = []
ships = []

app = Game()
menu = Menu()
menu.add_command(label='New Game', command=app.new_game)
app['menu'] = menu

frm_user_field = Frame(height=400, width=400)
btn_check = Button(text='Place ship', command=place)

app.mainloop()
