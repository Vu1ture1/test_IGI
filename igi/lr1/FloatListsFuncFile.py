import GeneratorAndDecoratorFile

def float_list_function():
    """This function finds the number of the minimum negative list element and the sum of the list elements located
    between the first and second negative elements."""
    print("\nInput float numbers: (enter 'q' for exit inputting)")
    flist = list(GeneratorAndDecoratorFile.input_generator())

    print(f"\nList: {flist}")

    min_neg_index = None
    min_neg_value = None

    for i, value in enumerate(flist):
        if value < 0 and (min_neg_value is None or value < min_neg_value):
            min_neg_value = value
            min_neg_index = i

    if min_neg_value != None and min_neg_index != None:
        print(f"Index of minimal negative number: index {min_neg_index}, value {flist[min_neg_index]}\n")
    else:
        print("Input not have any negative number")
        return

    all_negative = [i for i, value in enumerate(flist) if value < 0]

    sum_ = 0

    if len(all_negative) >= 2:
        sum_ = sum(flist[all_negative[0] + 1:all_negative[1]])
    else:
        print("Input flist not have 2 negative numbers")
        return

    print(f"Sum between two first negative numbers: sum {sum_}")