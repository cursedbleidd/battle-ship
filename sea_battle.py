from tkinter import *
from tkinter import messagebox


class Game(Tk):
    def __init__(self, screenName=None, baseName=None, className='Tk',
                 useTk=1, sync=0, use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.player1 = Player(1, self, name='Player1')
        self.player2 = Player(2, self, name='Player2')
        self.title('BattleShip')
        self.resizable(0, 0)
        with open('rules.txt', 'r', encoding='utf-8') as f:
            self.rules = Label(text=f.read())
        menu = Menu()
        self['menu'] = menu
        menu.add_command(label='New game', command=self.new_game)
        self.rules.pack()
        self.btn_place = Button(text='Place ship', padx=10, pady=6)

    def delete_players(self):
        for player in self.player1, self.player2:
            player.board.destroy()
        del self.player1, self.player2

    def new_game(self):
        print(self.player1, self.player2)
        self.delete_players()
        self.player1 = Player(1, self, name='Player1')
        self.player2 = Player(2, self, name='Player2')
        self.rules.pack_forget()
        self.btn_place.config(command=self.player1.board.place)
        self.btn_place.pack(side=BOTTOM)
        self.player1.board.pack()
        messagebox.showinfo('', f'{self.player2.name} goes for a walk')

    def ready(self, player):
        if player.id == 1:
            self.player1.board.pack_forget()
            self.btn_place.config(command=self.player2.board.place)
            self.player2.board.pack()
            messagebox.showinfo('', f'{self.player1.name} goes for a walk')
        elif player.id == 2:
            self.player2.board.pack_forget()
            self.btn_place.pack_forget()
            self.game()
        else:
            messagebox.showerror('Error', 'Вы не готовы!')

    def game(self):
        pass


class Board(Frame):
    def __init__(self, player, matrix=[], **kw):
        super().__init__(**kw)
        self.player = player
        self.selected_cells = []
        self.placed_cells = []
        self.ships = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
        self.matrix = matrix
        for y in range(10):
            line = []
            for x in range(10):
                cell = Cell(master=self, pos=(x, y), width=40, height=40, relief=GROOVE, bg='#fff', borderwidth=1)
                cell.grid(row=y, column=x)
                line.append(cell)
            self.matrix.append(line)

    def place(self):
        flag = True
        if len(self.selected_cells) == self.ships[0]:
            set_of_x = set()
            set_of_y = set()
            coordinates = []
            for cell in self.selected_cells:
                coordinates.append(cell.pos)
                set_of_x.add(cell.pos[0])
                set_of_y.add(cell.pos[1])
            coordinates.sort()
            print('!', coordinates, set_of_x, set_of_y, sep='\n')  # debug
            for i in range(self.ships[0] - 1):
                if not ((len(set_of_x) == 1 or len(set_of_y) == 1)
                        and (abs(coordinates[i][0] - coordinates[i + 1][0]) == 1
                             or abs(coordinates[i][1] - coordinates[i + 1][1]) == 1)):
                    messagebox.showerror('Error', 'Incorrect form of ship')
                    flag = False
                    break
            if flag:
                poses = self.placed_cells.copy()
                for pos in coordinates:
                    poses.remove(pos)
                for pos in coordinates:
                    for cell in poses:
                        if (abs(pos[0] - cell[0]) == 1 and abs(pos[1] - cell[1]) == 1) \
                                or (pos[0] - cell[0] == 0 and abs(pos[1] - cell[1]) == 1) \
                                or (abs(pos[0] - cell[0]) == 1 and pos[1] - cell[1] == 0):
                            print(self.placed_cells)  # debug
                            print(poses)  # debug
                            flag = False
                            messagebox.showerror('Error', 'Incorrect positioning')
                            break
                    if not flag:
                        break
        elif self.ships[0] > len(self.selected_cells):
            messagebox.showerror('Error', 'Select more cells')
            flag = False
        else:
            messagebox.showerror('Error', 'Too many selected cells')
            flag = False
        if flag:
            self.ships.pop(0)
            for cell in self.selected_cells:
                cell.status = 'part'
            self.selected_cells.clear()
        else:
            self.unselect_cells()
        if len(self.ships) == 0:
            self.player.master.ready(self.player)

    def unselect_cells(self):
        for cell in self.selected_cells.copy():
            cell.select('<Button-1>')


class Cell(LabelFrame):
    def __init__(self, pos, status='empty', **kw):
        super().__init__(**kw)
        self.pos = pos
        self.status = status
        self.bind('<Button-1>', self.select)

    def select(self, event):
        if self.status == 'empty':
            self.status = 'filled'
            self['bg'] = '#000'
            self.master.selected_cells.append(self)
            self.master.placed_cells.append(self.pos)
        elif self.status == 'filled':
            self.status = 'empty'
            self['bg'] = '#fff'
            self.master.selected_cells.remove(self)
            self.master.placed_cells.remove(self.pos)


class Player:
    def __init__(self, id, master, name='Player'):
        self.master = master
        self.name = name
        self.id = id
        self.board = Board(self, height=400, width=400)


if __name__ == '__main__':
    Game().mainloop()
