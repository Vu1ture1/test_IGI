def cycle_function():
    """Function that create a loop that takes integers and subtracts them from 10000. Ends with a negative result."""
    num = 10000

    print("Input any whole numbers:")

    while num >= 0:
        try:
            inp = int(input())
        except ValueError:
            print("Not whole number\n")
            continue

        num -= inp

        if num == 0:
            print("\nRemain number already == 0")
            return
        elif num < 0:
            print("\nRemain number already < 0")
            return
        else:
            print(f"Remain number = {num}\n")