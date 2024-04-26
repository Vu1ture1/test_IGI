import math

def pw_function(x, eps=0.1):
    """Function that calculating the value of a function using a power series expansion of the function(ln(1-x)), where
    |x| < 1, takes two arguments x and eps - accuracy for result."""
    if math.fabs(x) >= 1:
        print("|x| >= 1")
        return
    sum = 0.0
    n = 1
    curr = 0.0
    while n < 501:
        curr = -(math.pow(x, n)/n)
        if math.fabs(curr) <= eps:
            sum += curr
            break
        else:
            sum += curr
            n += 1

    rou =  int(math.log10(eps)*-1)

    sum = round(sum, rou)
    Fx = round(math.log(1-x, math.e), rou)


    print(f"|{'x':<5}|{'n':<{len(str(n))+1}}|{'F(x)':<{(rou + 6)}}|{'Math.F(x)':<{(rou + 8)}}|{'epsilon':<{(rou + 7)}}|")
    print(f"|{x:<5}|{n:<{len(str(n))+1}}|{sum:<{(rou + 6)}}|"
          f"{Fx:<{(rou + 8)}}|{eps:<{(rou + 7)}}|")