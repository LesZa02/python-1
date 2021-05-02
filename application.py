import tkinter.ttk as ttk
import random
from pole import *


class Application(tk.Frame):
    def __init__(self, root):
        """
        Конструктор наследника
        Определены константы выйгрыша,
        константы приоритетных угловых полей,
        константы не угловых полей.
        Вызывается функция, конструирующая клетки.
        """
        super(Application, self).__init__(root, width=field_w, height=field_h)
        self.pack()
        self.board_start = [' '] * field_size**2
        self.start_pole = [x for x in range(field_size**2)]
        self.create_widgets()

    def create_widgets(self):
        """
        Функция, создающая клетки поля
        Делает заливку фона,
        создает клетки поля,
        создает кнопку старт,
        создает поле с посланием,
        создает выбор хода.
        """
        self.fill = tk.Label(self, bg=field_color, width=field_w, height=field_h)
        self.fill.place(x=0, y=0)

        # клетки
        self.pole = {}
        for num in range(field_size**2):
            self.pole[num] = Pole(self, num)

        # кнопка старт
        self.button_start = tk.Button(self, text="Start", bg=but_color)
        self.button_start.bind("<Button-1>", self.start)
        self.button_start.place(x=but_place_x, y=but_plce_y, width=but_width)

        # Статус игры
        self.status = tk.StringVar()
        status_lbl = tk.Label(self, textvariable=self.status, bg=but_color,
                              bd=2, width=st_width, height=st_height, anchor='center')
        status_lbl.place(x=st_x, y=st_y)
        self.status.set('Press "start')

        # Выбор хода
        frame = tk.LabelFrame(self, text=" Want to go ", width=frame_width, height=frame_height, bg=but_color, bd=0)
        frame.place(x=frame_x, y=frame_y)
        self.combobox = ttk.Combobox(self, values=[u'first', u'second'])
        self.combobox.current(0)
        self.combobox.place(x=comb_x, y=comb_y)
        self.widgets = [self.combobox, self.button_start]

    def start(self, *args):
        """
        Функция, запускающая игру
        Создает список свободных клеток,
        создаем поле
        """
        # Основные поля
        self.next_moves = None
        self.end = False
        self.free_pos = self.start_pole[:]
        self.board = self.board_start[:]
        self.status.set('Game on')
        for i in range(field_size**2):
            cur_pole = self.pole[i]
            cur_pole.bind()
            cur_pole.mark_pole('')
            cur_pole.change_color(pole_color)
        if self.combobox.get() == 'second':
            self.turn_pc()
        self.combobox.config(state=tk.DISABLED)
        self.button_start.config(state=tk.DISABLED)
        self.button_start.unbind("<Button-1>")

    def check_win(self, sign, move):
        x, y = move % field_size, (move // field_size) * field_size
        self.wins = []
        if sign == self.board[y] and sign == self.board[y + 1] and sign == self.board[y + 2]:
            self.wins = [y, y + 1, y + 2]
        if sign == self.board[x] and sign == self.board[x + 3] and sign == self.board[x + 6]:
            self.wins = [x, x + 3, x + 6]
        if sign == self.board[0] and sign == self.board[4] and sign == self.board[8]:
            self.wins = [0, 4, 8]
        if sign == self.board[2] and sign == self.board[4] and sign == self.board[6]:
            self.wins = [2, 4, 6]
        return len(self.wins) == field_size

    def is_over(self, sign, move):
        """
        Эта функция, определяющая, закончена игра или нет
        Проверяет, заполнена ли хотя бы одна выйгрышная ситуация одним знаком.
        Если да, то подсвечивает данную конфигурацию соответствующим цветом.
        Если свободных клеток не осталось, то ничья.
        """
        if self.check_win(sign, move):
            color = 'green' if sign == 'x' else 'red'
            for i in self.wins:
                cur_pole = self.pole[i]
                cur_pole.change_color(color)
            for i in self.free_pos:
                self.pole[i].unbind()
            if sign == 'x':
                self.status.set('Woow! You are a champion!')
            else:
                self.status.set('Ooops, you lose')
            self.end = True
            self.combobox.config(state=tk.NORMAL)
            self.button_start.config(state=tk.NORMAL)
            self.button_start.bind("<Button-1>", self.start)
            return
        if not self.free_pos:
            self.status.set('Hmm... We don\'t have a winner')
            self.end = True
            for i in range(9):
                cur_pole = self.pole[i]
                cur_pole.change_color('yellow')
            self.combobox.config(state=tk.NORMAL)
            self.button_start.config(state=tk.NORMAL)
            self.button_start.bind("<Button-1>", self.start)

    def find_win_move(self):
        """
        Функция, ищущая выгрышный ход.
        Если выйгрышный ход есть, возвращет его, если нет, то None.
        """
        for sign in ['o', 'x']:
            for move in self.free_pos:
                self.board[move] = sign
                if self.check_win(sign, move):
                    return move
                self.board[move] = ''
        return None

    def turn_pc(self):
        """
        Эта функция реализует  ход ИИ
        Если возможен ход, ведущий к выйгрышу, то делается он.
        Если возможен ход соперника, ведущий к выйгрышу соперника, то ИИ делает ход туда, чтобы помешать.
        Если таких ходов нет, то делается стандартный ход.
        """
        move = self.find_win_move()
        if move is None:
            move = random.choice(self.free_pos)
        self.do_move(move, 'o')

    def do_move(self, move, sign):
        """
        Функция, делающая ход.
        Ставит на клетке знак,
        деактивирует её,
        удаляет из списка свободных клеток,
        проверяет не закончена ли игра.
        """
        self.pole[move].unbind()
        self.pole[move].mark_pole(sign)
        self.board[move] = sign
        self.free_pos.remove(move)
        self.is_over(sign, move)
