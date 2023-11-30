"""
Напишіть програму, де клас «геометричні фігури» (Figure) містить властивість
color з початковим значенням white і метод для зміни кольору фігури, а його
підкласи «овал» (Oval) і «квадрат» (Square) містять методи __init__ для
завдання початкових розмірів об'єктів при їх створенні.
"""


class Figure:
    def __init__(self) -> None:
        self.color = 'white'

    def set_color(self, color) -> None:
        self.color = color


class Oval(Figure):
    def __init__(self, x_param=1., y_param=1., radius=1.) -> None:
        self.x_param = x_param
        self.y_param = y_param
        self.radius = radius
        super().__init__()


class Square(Figure):
    def __init__(self, border) -> None:
        self.border = border
        super().__init__()
