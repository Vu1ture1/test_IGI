import PowerSeriesFuncFile
import CycleFuncFile
import StringAnalyseFile
import StringPermanentAnalyseFile
import FloatListsFuncFile
import GeneratorAndDecoratorFile

#Made by student 'Mikhail Kupreichyk' from group 253503.

def main():
      while True:

            print("Choose option between 1-5: \n1) PowerSeriesFunction(First task)\n2) CycleFunction(Second task)\n3) "
                  "InputStringAnalyseFunction"
                  "(Third task)\n4) PermanentStringAnalyseFunction(Four task)\n5) FloatListFunclion(Five task)\nOr "
                  "just 'q' for exit\n")

            inp = 0

            print("option: ")
            while True:
                  try:
                        inp = input()

                        if inp == "q":
                              return

                        inp = int(inp)

                        if inp < 0 or inp > 5:
                              continue
                        else:
                              break
                  except ValueError:
                        print("Not correct option\n")
                        continue

            print("\n")

            if inp == 1:
                  print("Enter x: ")
                  x = 0.0
                  eps = 0.0
                  while True:
                        try:
                              var = input()

                              x = float(var)
                              break
                        except ValueError:
                              print("Not any number\n")
                              continue

                  print("\nEnter epsilon: ")

                  while True:
                        try:
                              var = input()

                              eps = float(var)
                              break
                        except ValueError:
                              print("Not any number\n")
                              continue

                  PowerSeriesFuncFile.pw_function(x, eps)
                  print("\n")
            elif inp == 2:
                  foo = GeneratorAndDecoratorFile.decorator(CycleFuncFile.cycle_function)
                  foo()
                  print("\n")
            elif inp == 3:
                  foo = GeneratorAndDecoratorFile.decorator(StringAnalyseFile.find_coin)
                  foo()
                  print("\n")
            elif inp == 4:
                  foo = GeneratorAndDecoratorFile.decorator(StringPermanentAnalyseFile.find_substrings)
                  foo()
                  print("\n")
            elif inp == 5:
                  foo = GeneratorAndDecoratorFile.decorator(FloatListsFuncFile.float_list_function)
                  foo()
                  print("\n")

main()