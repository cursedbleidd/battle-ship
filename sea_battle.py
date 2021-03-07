from tkinter import *
from tkinter import messagebox


class Game(Tk):
    def __init__(self, screenName=None, baseName=None, className='Tk',
                 useTk=1, sync=0, use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.mode = 'pc'
        self.turn = True
        self.count = 0
        self.iconbitmap('icon.ico')
        self.title('BattleShip')
        self.resizable(0, 0)
        with open('rules.txt', 'r', encoding='utf-8') as f:
            self.rules = Label(text=f.read(), justify=LEFT)
        menu = Menu()
        self['menu'] = menu
        menu.add_command(label='New game', command=self.new_game)
        menu.add_command(label='Change mode', command=self.change_mode)
        self.rules.grid(row=0, column=0)
        self.btn_place = Button(text='Place ship', padx=10, pady=6)
        self.labels = []
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for id, letter in enumerate(letters, 1):
            self.labels.append(((Label(text=letter, justify=CENTER), id), Label(text=id, justify=CENTER)))

    def delete_players(self):
        try:
            for player in self.player1, self.player2:
                player.board.destroy()
            del self.player1, self.player2
        except AttributeError:
            pass

    def new_game(self):
        self.delete_players()
        self.player1 = Player(1, self, name='Player1')
        self.player2 = Player(2, self, name='Player2')
        self.label = Label(text=f'{self.player1.name}', justify=CENTER)
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for label in self.labels:
            label[0][0].grid_forget()
            label[1].grid_forget()
        for id, letter in enumerate(letters, 1):
            Label(text=letter, justify=CENTER).grid(row=2, column=(id+1))
            Label(text=id, justify=CENTER).grid(row=(id+2), column=1, padx=5)
        self.count = 0
        self.rules.grid_forget()
        self.label.grid(row=1, column=1, columnspan=11)
        self.btn_place.config(command=self.player1.board.place)
        self.btn_place.grid(row=13, column=5, pady=10, columnspan=3)
        self.player1.board.grid(row=3, column=2, rowspan=10, columnspan=10)
        if self.mode == 'pc':
            messagebox.showinfo('', f'{self.player2.name} goes for a walk')

    def ready(self, player):
        if player.id == 1 and self.mode == 'pc':
            self.player1.board.grid_forget()
            self.btn_place.config(command=self.player2.board.place)
            self.label.config(text=f'{self.player2.name}')
            self.player2.board.grid(row=3, column=2, rowspan=10, columnspan=10)
            messagebox.showinfo('', f'{self.player1.name} goes for a walk')
        elif player.id == 1 and self.mode == 'multi':
            self.label.grid_forget()
            self.btn_place.grid_forget()
            self.player1.board.grid_forget()
            self.game()
        else:
            self.label.grid_forget()
            self.player2.board.grid_forget()
            self.btn_place.grid_forget()
            self.game()

    def change_mode(self):
        if messagebox.askyesno('', 'Change game mode?'):
            if self.mode == 'multi':
                self.mode = 'pc'
            else:
                self.mode = 'multi'
            self.new_game()

    def game(self):
        for player in self.player1, self.player2:
            player.board.color()
            if self.mode == 'multi':
                player.board.grid(row=player.parameters[0], column=player.parameters[1],
                                  rowspan=player.parameters[2], columnspan=player.parameters[2])
        if self.mode == 'pc':
            self.change_board()
        else:
            for label in self.labels:
                label[0][0].grid(row=2, column=label[0][1]+12)
                label[1].grid(row=(2+int(label[1]['text'])), column=12)

    def change_board(self):
        (self.player1, self.player2)[not self.turn].board.grid_forget()
        (self.player1, self.player2)[self.turn].board.grid(row=3, column=2, rowspan=10, columnspan=10)

    def shoot(self, change):
        players = [self.player1, self.player2]
        if players[self.turn].board.ship_check():
            messagebox.showinfo('', 'Ship destroyed')
        if self.mode == 'pc' and change:
            self.turn = not self.turn
            self.change_board()
        for player in players:
            if len(player.board.placed_cells) == 0 and not (player.id == 2 and self.mode == 'multi') or \
                    (self.count == 20 and self.mode == 'multi' and player.id == 2):
                if messagebox.askyesno('Win', f'{players[not self.turn].name} won\nStart a new game?'):
                    self.new_game()
                else:
                    self.destroy()


class Board(Frame):
    def __init__(self, player, matrix=[], **kw):
        super().__init__(**kw)
        self.player = player
        self.selected_cells = []
        self.placed_cells = []
        self.boats = []
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
            self.boats.append(Ship(self.selected_cells.copy()))
            self.ships.pop(0)
            for cell in self.selected_cells:
                cell.status = 'ship piece'
            self.selected_cells.clear()
        else:
            self.unselect_cells()
        if len(self.ships) == 0:
            self.player.master.ready(self.player)

    def unselect_cells(self):
        for cell in self.selected_cells.copy():
            cell.select('<Button-1>')

    def color(self):
        for line in self.matrix:
            for cell in line:
                if cell.status == 'empty':
                    cell.status = 'sea'
                elif cell.status == 'ship piece':
                    cell.status = 'part'
                    if self.player.master.mode == 'pc':
                        cell['bg'] = '#fff'

    def ship_check(self):
        ships = self.boats.copy()
        for ship in ships:
            if ship.check():
                self.boats.remove(ship)
                return True
        return False


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
        elif self.status == 'sea':
            self.status = 'missed'
            self['bg'] = 'blue'
            if self.master.player.master.mode == 'pc':
                messagebox.showinfo('', 'You have missed')
            self.master.player.master.shoot(True)
        elif self.status == 'part':
            self.status = 'destroyed'
            self['bg'] = 'red'
            self.master.placed_cells.remove(self.pos)
            self.master.player.master.shoot(False)
        elif self.status in ('missed', 'destroyed'):
            if self.status == 'missed' and self.master.player.master.mode == 'multi' and self.master.player.id == 2:
                self.status = 'destroyed'
                self['bg'] = 'red'
                self.master.player.master.count += 1
                self.master.player.master.shoot(False)
            else:
                messagebox.showerror('Error', 'You have already shot there')


class Ship:
    def __init__(self, cells):
        self.cells = cells

    def check(self):
        for cell in self.cells:
            if cell.status != 'destroyed':
                return False
        return True


class Player:
    def __init__(self, id, master, name='Player'):
        self.master = master
        self.name = name
        self.id = id
        self.parameters = (3, 2, 10)
        if self.id == 2:
            self.parameters = (3, 13, 10)
        self.board = Board(self, height=400, width=400)


if __name__ == '__main__':
    Game().mainloop()
