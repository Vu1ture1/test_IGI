from abc import ABC, abstractmethod, abstractproperty
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
import math

#Creator Mikhail Kupreichyk from group 253503
#version 1
#Lab number 4
#08.05.2024
#Variant 14
class GeometricFigure(ABC): #Abstract class figure
    @abstractmethod
    def area_calc(self):
        pass

class FigureColor:
    def __init__(self, color):
         self._color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val):
        self._color = val

class CircleInSquare(GeometricFigure):
    def __init__(self, radius, color):
        self.color = FigureColor(color)
        self.radius = radius
        self.side = radius * 2

    def area_calc(self):
        """Calculate area of circle and square"""
        return (2 * (self.radius ** 2)), (2 * math.pi * self.radius)


    def plot_figure(self):
        """Method for plotting figure"""
        fig, ax = plt.subplots()

        x_y_c = (self.radius)

        rect = patches.Rectangle((0, 0), self.side, self.side, fill=False, color=self.color.color)
        circle = patches.Circle((x_y_c, x_y_c), self.radius, fill=True, color=self.color.color)

        ax.add_patch(rect)
        ax.add_patch(circle)

        ax.text(self.radius, self.side + self.radius * 0.2, f'Square, side = {self.side}', ha='center', va='center', color='black')
        if self.color.color == 'black':
            ax.text(x_y_c, x_y_c, f'Circle, R = {self.radius}', ha='center', va='center', color='white')
        else:
            ax.text(x_y_c, x_y_c, f'Circle, R = {self.radius}', ha='center', va='center', color='black')

        #ax.grid(True)

        ax.set_xlim([0, self.radius*3])
        ax.set_ylim([0, self.radius*3])

        plt.xlabel('x')

        ax.set_aspect('equal')

        plt.savefig('D:\\253503_KUPREICHYK_14\igi\plot_fig.png')  # Save to file

        plt.show()

def input_val():
    radius = 0
    color_str = ''

    while True:
        try:
            radius = (float)(input("Enter radius: "))

            if(radius <= 0):
                print("Not correct input!!!")
                continue

            color_str = (input("Enter color(black, red, green, gray): "))

            if(color_str != 'black' and color_str != 'red' and color_str != 'green' and
               color_str != 'gray'):
                print("Not correct input!!!")
                continue
            break

        except ValueError:
            print("Not correct input!!!")
            continue

    return radius, color_str


def main():
    while True:
        r, col = input_val()

        var = CircleInSquare(r, col)

        S1, S2 = var.area_calc()

        print(f"Area of square = {S1}, of circle = {S2}, of all figure = {S1 + S2}")

        var.plot_figure()

        print("If want exit enter \'e\':")

        str = input()

        if(str == 'e'):
            break


main()
if __name__ == "main":
    main()