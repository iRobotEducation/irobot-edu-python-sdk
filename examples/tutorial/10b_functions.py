#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

import random

# Let's explore other interesting things about Python functions.

workdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']


def food_per_workday():
    return ['Rice', 'Pizza', 'Salad', 'Spaghetti', 'Potatoes']


def print_menu():
    menu = food_per_workday()
    for i in range(len(workdays)):
        print(workdays[i] + ': ' + menu[i])


print_menu()
print()

# Python allows functions to be redefined on the fly; here we redefine food_per_workday() !


def food_per_workday():
    lst = ['Rice', 'Pizza', 'Salad', 'Spaghetti', 'Potatoes']
    random.shuffle(lst)
    return lst


print('--- Shuffled version: ---')

# Calling print_menu() will use the most recent version of food_per_workday, ignoring any previous definitions.
print_menu()
print()

# Finally:
# - Functions can be nested; functions defined within other functions cannot be called
#   from outside of the functions in which they were defined (this is called "scope").
# - Functions can have default values for their parameters.


def print_menu(shuffle=False):
    def nested_food_per_workday():  # We call it differently just to try if calling it will trigger an error.
        return ['Rice', 'Pizza', 'Salad', 'Spaghetti', 'Potatoes']

    menu = nested_food_per_workday()
    if shuffle:
        random.shuffle(menu)

    for i in range(len(workdays)):
        print(workdays[i] + ': ' + menu[i])


print_menu()
print()
print('--- Shuffled version: ---')
print_menu(True)
# nested_food_per_workday()  # 📛 Error! See https://docs.python.org/3/reference/executionmodel.html#resolution-of-names
