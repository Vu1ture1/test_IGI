import math
import matplotlib.pyplot as plt
import numpy as np
import statistics

#Creator Mikhail Kupreichyk from group 253503
#version 1
#Lab number 4
#08.05.2024
#Variant 14
class Approx:
    def __init__(self, x, eps, max_num_of_itt):
        self.x = x
        self.eps = eps
        self.max_num_of_itt = max_num_of_itt
        self.subseq = []
        self.sum = 0
        self.n = 0

    def pw_function(self):
        """Function that calculating the value of a function using a power series expansion of the function(ln(1-x)), where
        |x| < 1, takes two arguments x and eps - accuracy for result."""
        if math.fabs(self.x) >= 1:
            print("|x| >= 1")
            return
        sum = 0.0
        n = 1
        subseq = []
        curr = 0.0
        while n < self.max_num_of_itt:

            curr = -(math.pow(self.x, n) / n)

            if math.fabs(curr) <= self.eps:
                subseq.append(sum)
                sum += curr
                subseq.append(sum)
                n += 1
                break
            else:
                subseq.append(sum)
                sum += curr
                n += 1

        self.subseq = subseq
        self.sum = sum
        self.n = n

        rou = int(math.log10(self.eps) * -1)

        sum_p = round(sum, rou)

        Fx = round(math.log(1 - self.x, math.e), rou)

        print(
            f"|{'x':<5}|{'n':<{len(str(n)) + 1}}|{'F(x)':<{(rou + 6)}}|{'Math.F(x)':<{(rou + 8)}}|{'epsilon':<{(rou + 7)}}|")
        print(f"|{self.x:<5}|{n:<{len(str(n)) + 1}}|{sum_p:<{(rou + 6)}}|"
              f"{Fx:<{(rou + 8)}}|{self.eps:<{(rou + 7)}}|")

        return subseq, sum, n

class MixinStats:
    def all_stats(self):
        """Calculate statistics for sequence"""
        mode = statistics.mode(self.subseq)
        mean = statistics.mean(self.subseq)
        median = statistics.median(self.subseq)
        disp = statistics.variance(self.subseq)
        standard_dev = statistics.stdev(self.subseq)

        return mode, mean, median, disp, standard_dev

class ApproxPlot(Approx, MixinStats):
    def __init__(self, x, eps, max_num_of_itt):
        super().__init__(x, eps, max_num_of_itt)

    def plots(self):
        """Method for drawing plot"""
        x_values = np.linspace(-0.99, 0.99, 100)
        y_values = np.log(1 - x_values)
        approx_values = [-self.x]

        plt.plot(x_values, y_values, label='Math F(x)')

        plt.plot(x_values, np.interp(x_values, np.linspace(-0.99, 0.99, len(self.subseq)), self.subseq),
                 label=f'F(x) (n={self.n})')

        plt.xlabel('x')

        plt.ylabel('Value')

        plt.legend()

        plt.grid(True)

        plt.savefig('D:\\253503_KUPREICHYK_14\igi\plot.png')  # Save to file

        plt.title('Approximation of Ln(1-x)')

        plt.show()

    @property
    def x_val(self):
       return self.x

    @x_val.setter
    def x_val(self, val):
        if math.fabs(val) >= 1:
            print("|x| >= 1")
            return
        else:
            self.x = val
    @property
    def eps_val(self):
        return self.eps

    @eps_val.setter
    def eps_val(self, val):
        self.eps = val

def input_val():
    x = 0
    eps = 0.0
    n = 0

    while True:
        try:
            x = (float)(input("Enter x: "))

            if math.fabs(x) >= 1:
                print("|x| >= 1")
                print("Not correct input!!!")
                continue

            eps = (float)(input("Enter epsilon: "))

            if(eps > 0.1 or eps <= 0):
                print("Not correct input!!!")
                continue

            n = (int)(input("Enter n: "))

            if (n <= 0):
                print("Not correct input!!!")
                continue

            break

        except ValueError:
            print("Not correct input!!!")
            continue

    return x, eps, n

def main():
    while True:
        a1, a2, a3 = input_val()

        var = ApproxPlot(a1, a2, a3)

        var.pw_function()

        print("(mode, mean, median, disp, standard_dev):")
        print(var.all_stats())

        var.plots()

        str = input("If want to exit enter \'e\':")

        if str == 'e':
            break



if __name__ == '__main__':
    main()
