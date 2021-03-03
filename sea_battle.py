from tkinter import *
from tkinter import messagebox


class Game(Tk):
    @staticmethod
    def new_game():
        global num_ships, selected_cells
        num_ships = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
        frm_user_field.pack(side=TOP, padx='10', pady='10')
        for y in range(10):
            for x in range(10):
                Cell(pos=(x, y), master=frm_user_field, width=40, height=40, bg='#fff', relief=GROOVE, borderwidth=1)\
                    .grid(row=y, column=x)
        btn_check.pack(side=BOTTOM, pady='10')

    @staticmethod
    def game():
        frm_user_field.pack(side=LEFT, padx='10', pady='10')
        frm_enemy_field.pack(side=RIGHT, padx='10', pady='10')
        for y in range(10):
            for x in range(10):
                Cell(pos=(x, y), status=5, master=frm_enemy_field, width=40, height=40, bg='#fff', relief=GROOVE,
                     borderwidth=1).grid(row=y, column=x)


class Cell(LabelFrame):
    def __init__(self, pos, status=0, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.pos = pos
        self.status = status
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
        print(self.pos)  # debug
        print(len(selected_cells))

    def unselect(self):
        selected_cells.remove(self)
        self['bg'] = '#fff'
        self.status = 0


class Ship:
    def __init__(self, cells):
        self.cells = cells


def place():
    global selected_cells, num_ships, ships
    flag = True
    if num_ships[0] == len(selected_cells):
        set_of_y = set()
        set_of_x = set()
        coordinates = []
        for cell in selected_cells:
            coordinates.append(cell.pos)
            set_of_x.add(cell.pos[0])
            set_of_y.add(cell.pos[1])
        coordinates.sort()
        for i in range(num_ships[0] - 1):
            if (len(set_of_x) == 1 or len(set_of_y) == 1) \
                and (abs(coordinates[i][0] - coordinates[i + 1][0]) == 1
                     or abs(coordinates[i][1] - coordinates[i + 1][1]) == 1):
                flag = True
            else:
                messagebox.showerror('Error', 'Incorrect positioning')
                flag = False
                break
    elif num_ships[0] > len(selected_cells):
        messagebox.showerror('Error', 'Select more cells')
        flag = False
    else:
        messagebox.showerror('Error', 'Too many selected cells')
        flag = False
    if flag:
        ships.append(Ship(selected_cells))
        num_ships.pop(0)
        selected_cells.clear()
    else:
        unselect_cells(selected_cells)
    if len(num_ships) == 0:
        app.game()
        btn_check.destroy()


def unselect_cells(cells):
    for cell in cells.copy():
        cell.unselect()
    cells.clear()


num_ships = []
selected_cells = []
ships = []

app = Game()
menu = Menu()
menu.add_command(label='New Game', command=app.new_game)
app['menu'] = menu

frm_user_field = Frame(height=400, width=400)
frm_enemy_field = Frame(height=400, width=400)
btn_check = Button(text='Place ship', command=place, padx=10, pady=5)

app.mainloop()
