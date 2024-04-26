import time
def input_generator():
    """Generator for input numbers."""
    while True:
        try:
            inp = input()

            if inp == "q":
                return

            inp = float(inp)

            yield inp
        except ValueError:
            print("Not any number\n")
            continue


def decorator(func):
    """Simple decorator for any function, print work time of function"""
    def dec_func():
        print("Process started:")
        start = time.time()
        func()
        end = time.time()
        print(f"\nProcess ended: Time = {end - start}")
    return dec_func