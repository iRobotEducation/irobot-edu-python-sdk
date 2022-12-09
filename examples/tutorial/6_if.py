#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

# If you need to make a decision, use the "if" keyword. Try running the following program multiple times:

from random import random

print()
guess = random()
print('guess =', guess)

# In Python, indentation matters, and it will affect the meaning of your program:
print()
print('What will we eat for lunch today?')
if 0.0 <= guess < 0.3:
    print("Let's eat a salad!")
elif 0.3 <= guess < 0.8:
    print("Let's have a", end = ' ')
    which_model = random()
    if which_model < 0.5:
        print('Neapolitan', end = ' ')
    else:
        print('Fugazzeta', end = ' ')
    print('pizza!')
else:
    print("Let's eat rice!")

print()
print('Try running this program again...')
