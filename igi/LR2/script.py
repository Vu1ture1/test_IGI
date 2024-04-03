import os
from circle import area
from square import perimeter

my_var = float(os.getenv('var'))



print("S|circle|(2) = ")
print(area(my_var))

print("\n")
print("P|square|(2) = ")
print(perimeter(my_var))