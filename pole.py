import tkinter as tk
from parameters import *
import time


class Pole:

    def __init__(self, root, num):
        '''
        Функция инициализации
        :param num - номер клетки, w - ширина, h - высота, padx - сдвиг по x,
        pady - сдвиг по y, b - расстояние между клетками
        '''
        self.root = root
        self.num = num
        self.sign = tk.StringVar()
        # поля игры
        self.lbl = tk.Label(self.root, textvariable=self.sign,
                            font="Modern 55", bg=pole_color)
        self.lbl.place(x=padx + (num % field_size) * (pole_w + space),
                       y=pady + (num // field_size) * (pole_h + space), width=pole_w, height=pole_h)

    def mark_pole(self, mark):
        """ Функция помечает клетку """
        self.sign.set(mark)

    def stupid_user_move(self, *args):
        """ Вызывает функцию хода пользователя принажатии кнопки """
        self.root.do_move(self.num, 'x')
        self.root.update()
        time.sleep(0.5)
        if not self.root.end:
            self.root.turn_pc()

    def change_color(self, color):
        """ Меняетт цвет клетки """
        self.lbl.configure(bg=color)

    def unbind(self):
        """ Отвязывает функцию нажатия кнопки от кнопки """
        self.lbl.unbind("<Button-1>")

    def bind(self):
        """ Привязывает функцию нажатия кнопки к кнопке """
        self.lbl.bind("<Button-1>", self.stupid_user_move)

