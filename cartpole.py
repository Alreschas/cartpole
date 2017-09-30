
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import sys
import tkinter as tk


class cart_pole:
    def __init__(self):

        # environment
        self.dt = 0.01
        self.g = 9.81

        # input
        self.F = 0

        # cart
        self.l = 1
        self.M = 1
        self.x = 0
        self.xd = 0
        self.xdd = 0
        # pole
        self.m = 1
        self.th = np.pi + 0.01
        self.thd = 0
        self.thdd = 0
        self.friction = 0.1

    def simulateSingleStep(self):
        A = np.matrix([[self.m + self.M, self.m * self.l * np.cos(self.th)],
                       [np.cos(self.th), self.l]])
        b = np.matrix([[self.F + self.m * self.l * self.thd**2 * np.sin(self.th)],
                       [-self.friction * self.thd - self.g * np.sin(self.th)]])
        x = np.linalg.inv(A).dot(b)
        print(x)
        self.xdd = x[0, 0]
        self.xd += self.xdd * self.dt
        self.x += self.xd * self.dt

        self.thdd = x[1, 0]
        self.thd += self.thdd * self.dt
        self.th += self.thd * self.dt


class robot(cart_pole):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas

    def draw(self):
        self.offset_x = 800 / 2.
        self.offset_y = 400 / 2.

        self.cart_size_x = 70.
        self.cart_size_y = 50.

        self.tire_size = 15.

        self.cart_x = self.offset_x
        self.cart_y = self.offset_y

        self.tire1_x = self.cart_x + self.cart_size_x * 0.8
        self.tire2_x = self.cart_x - self.cart_size_x * 0.8
        self.tire_y = self.cart_y + self.cart_size_y

        self.ground_y = self.offset_y - self.cart_size_y

        self.ground = self.canvas.create_line(100, self.offset_y + self.cart_size_y, self.offset_x * 2 - 100, self.offset_y + self.cart_size_y, width=2.0, fill='#00ff00')
        self.tire1 = self.canvas.create_oval(self.tire1_x - 0.5 * self.tire_size, self.tire_y, self.tire1_x + 0.5 * self.tire_size, self.tire_y - self.tire_size, tag="oval", fill='#acb3ac')
        self.tire2 = self.canvas.create_oval(self.tire2_x - 0.5 * self.tire_size, self.tire_y, self.tire2_x + 0.5 * self.tire_size, self.tire_y - self.tire_size, tag="oval", fill='#acb3ac')
        self.cart = self.canvas.create_rectangle(self.cart_x - self.cart_size_x, self.cart_y - self.cart_size_y + self.tire_size, self.cart_x + self.cart_size_x, self.cart_y + self.cart_size_y - self.tire_size, fill="#c6c6c6")
        self.pole = self.canvas.create_line(self.cart_x, self.cart_y, self.cart_x + 200 * self.l * np.sin(self.th), self.cart_y + 200 * self.l * np.cos(self.th), width=2.0, fill='#5a43eb')

        print(self.canvas.winfo_width())

    def move(self):
        self.simulateSingleStep()

        self.cart_x = self.offset_x + self.x * 100
        self.tire1_x = self.cart_x + self.cart_size_x * 0.8
        self.tire2_x = self.cart_x - self.cart_size_x * 0.8

        self.canvas.coords(self.tire1, self.tire1_x - 0.5 * self.tire_size, self.tire_y, self.tire1_x + 0.5 * self.tire_size, self.tire_y - self.tire_size)
        self.canvas.coords(self.tire2, self.tire2_x - 0.5 * self.tire_size, self.tire_y, self.tire2_x + 0.5 * self.tire_size, self.tire_y - self.tire_size)

        self.canvas.coords(self.cart, self.cart_x - self.cart_size_x, self.cart_y - self.cart_size_y + self.tire_size, self.cart_x + self.cart_size_x, self.cart_y + self.cart_size_y - self.tire_size)
        self.canvas.coords(self.pole, self.cart_x, self.cart_y, self.cart_x + 200 * self.l * np.sin(self.th), self.cart_y + 200 * self.l * np.cos(self.th))


root = tk.Tk()

canvas = tk.Canvas(root, width=800, height=400)
# キャンバスバインド
rb = robot(canvas)
# canvas.place(x=0, y=0)
canvas.pack()
rb.draw()


def motion():
    rb.move()
    root.after(10, motion)


motion()
root.mainloop()
