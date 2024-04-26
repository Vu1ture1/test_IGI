def find_coin():
    """Function that finds number of ' ' and ',' symbols in input string."""
    print("Input any string:")
    string = input()

    print(f"\nNumber of ' ' in string: {string.count(' ')}\n")
    print(f"Number of ',' in string: {string.count(',')}")