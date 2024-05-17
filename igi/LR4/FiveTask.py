import numpy as np
import random
import math

#Creator Mikhail Kupreichyk from group 253503
#version 1
#Lab number 4
#08.05.2024
#Variant 14
class Statistics:
    def __init__(self):
        self.matrix = []

    def all_matrix_stats(self):
        """Calculate all matrix statistics"""
        if len(self.matrix) == 0:
            print("Enter matrix!!!")
            return

        list = self.matrix.flatten()
        mean = np.mean(list)
        median = np.median(list)
        var = np.var(list)
        std = np.std(list)

        return mean, median, var, std

class NumPyArray:
    def num_py_array(self, shape, val):
        """Method for forming shape and full it with value in argument"""
        return np.full(shape, val)

class MatrixCalculations(Statistics, NumPyArray):
    def __init__(self, n, m):
        self.n = n
        self.m = m
        super().__init__()

    def matrix_random_generator(self):
        """Creates matrix [n x m] and fill it with random nums in range [-1000; 1000]"""
        matr_list = []

        num_of_elem = self.n * self.m

        while num_of_elem > 0:
            matr_list.append(random.randint(-1000, 1000))
            num_of_elem -= 1

        self.matrix = np.array(matr_list).reshape(self.n, self.m)

        print(self.matrix)

    def sum_of_all_lower_diagonal_el(self):
        """Calculate sum of all elements that lower than main diagonal"""
        #print(self.matrix)

        el_sum = sum(self.matrix[np.tril_indices_from(self.matrix, -1)])

        #print(el_sum)

        return el_sum

    def diagonal_standard_deviation(self):
        """Method that calc standard deviation of diagonal with statistics and with programming formula"""
        #print(self.matrix)

        diagonal_elements = self.matrix.diagonal()

        x_av = np.sum(diagonal_elements) / len(diagonal_elements)

        std_val = round(math.sqrt(np.sum((diagonal_elements - x_av) ** 2) / (len(diagonal_elements))), 2)

        #print(std_val)

        #print(round(np.std(diagonal_elements), 2))

        return round(np.std(diagonal_elements), 2), std_val

def input_val():
    n = 0
    m = 0
    color_str = ''

    while True:
        try:
            n = (int)(input("Enter n: "))

            if(n <= 0):
                print("Not correct input!!!")
                continue

            m = (int)(input("Enter m: "))

            if (m <= 0):
                print("Not correct input!!!")
                continue

            break

        except ValueError:
            print("Not correct input!!!")
            continue

    return n, m
def main():
    while True:
        n, m = input_val()

        g = MatrixCalculations(n, m)

        print("Matrix: ")
        g.matrix_random_generator()

        print(f"Sum of all lower diagonal elements: {g.sum_of_all_lower_diagonal_el()}")

        print(f"St deviation of diagonal elements(func/formula): {g.diagonal_standard_deviation()}")

        print("[mean, median, var, std]:")

        print(g.all_matrix_stats())

        print("If want exit enter \'e\':")

        str = input()

        if(str == 'e'):
            break



main()
if __name__ == "main":
    main()