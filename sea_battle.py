from tkinter import *
from tkinter import messagebox


class Game(Tk):
    @staticmethod
    def new_game():
        global num_ships, selected_cells, matrix, selected_pos
        selected_pos = []
        matrix = []
        selected_cells = []
        num_ships = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
        frm_user_field.pack(side=TOP, padx='10', pady='10')
        frm_enemy_field.pack_forget()
        for y in range(10):
            line = []
            for x in range(10):
                cell = Cell(pos=(x, y), master=frm_user_field, width=40, height=40,
                            bg='#fff', relief=GROOVE, borderwidth=1)
                cell.grid(row=y, column=x)
                line.append(cell)
            matrix.append(line)

        btn_check.pack(side=BOTTOM, pady='10')

    @staticmethod
    def game():
        global matrix, matrix_enemy
        matrix_enemy = []
        frm_user_field.pack(side=LEFT, padx='10', pady='10')
        frm_enemy_field.pack(side=RIGHT, padx='10', pady='10')
        for y in range(10):
            line = []
            for x in range(10):
                if matrix[y][x].status == 1:
                    matrix[y][x].status = 6
                elif matrix[y][x].status == 0:
                    matrix[y][x].status = 5
                cell = Cell(pos=(x, y), status=5, master=frm_enemy_field, width=40, height=40,
                            bg='#fff', relief=GROOVE, borderwidth=1)
                cell.grid(row=y, column=x)
                line.append(cell)
            matrix_enemy.append(line)


class Cell(LabelFrame):
    def __init__(self, pos, status=0, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.status = status
        self.bind('<Button-1>', self.select)

    def select(self, event):
        global selected_cells, matrix
        if self.status == 1:
            self['bg'] = '#fff'
            self.status = 0
            selected_cells.remove(self)
            selected_pos.remove(self.pos)
        elif self.status == 0:
            self['bg'] = '#000'
            self.status = 1
            selected_cells.append(self)
            selected_pos.append(self.pos)
        print(self.pos)  # debug
        print(len(selected_cells))


class Ship:
    def __init__(self, cells):
        self.cells = cells


def place():
    global selected_cells, num_ships, ships, selected_pos
    poses = []
    flag = True
    print('!', *selected_cells)
    if num_ships[0] == len(selected_cells):
        set_of_y = set()
        set_of_x = set()
        coordinates = []
        for cell in selected_cells:
            coordinates.append(cell.pos)
            set_of_x.add(cell.pos[0])
            set_of_y.add(cell.pos[1])
        coordinates.sort()
        print('!', coordinates)
        for i in range(num_ships[0] - 1):
            if not ((len(set_of_x) == 1 or len(set_of_y) == 1)
                    and (abs(coordinates[i][0] - coordinates[i + 1][0]) == 1
                         or abs(coordinates[i][1] - coordinates[i + 1][1]) == 1)):
                messagebox.showerror('Error', 'Incorrect form of ship')
                flag = False
                break
        if flag:
            poses = selected_pos.copy()
            for pos in coordinates:
                poses.remove(pos)
            for pos in coordinates:
                in_flag = True
                if matrix[pos[1]][pos[0]].status == 0:
                    messagebox.showerror('Error', 'Already placed')
                    flag = False
                    break
                for cell in poses:
                    if (abs(pos[0] - cell[0]) == 1 and abs(pos[1] - cell[1]) == 1) \
                            or (pos[0] - cell[0] == 0 and abs(pos[1] - cell[1]) == 1) \
                            or (abs(pos[0] - cell[0]) == 1 and pos[1] - cell[1] == 0):
                        print(selected_pos)
                        print(poses)
                        flag = False
                        in_flag = False
                        messagebox.showerror('Error', 'Incorrect positioning')
                        break
                if not in_flag:
                    break
    elif num_ships[0] > len(selected_cells):
        messagebox.showerror('Error', 'Select more cells')
        flag = False
    else:
        messagebox.showerror('Error', 'Too many selected cells')
        flag = False
    if flag:
        ships.append(Ship(selected_cells))
        print(selected_pos)
        num_ships.pop(0)
        selected_cells.clear()
    else:
        unselect_cells(selected_cells)
    if len(num_ships) == 0:
        btn_check.pack_forget()
        app.game()


def unselect_cells(cells):
    for cell in cells.copy():
        cell.select('<Button-1>')
    cells.clear()


selected_pos = []
num_ships = []
selected_cells = []
ships = []
matrix = []
matrix_enemy = []

app = Game()
menu = Menu()
menu.add_command(label='New Game', command=app.new_game)
app['menu'] = menu
app.title('BattleShip')

frm_user_field = Frame(height=400, width=400)
frm_enemy_field = Frame(height=400, width=400)
btn_check = Button(text='Place ship', command=place, padx=10, pady=5)

app.mainloop()
