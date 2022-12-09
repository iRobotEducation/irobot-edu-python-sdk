#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

# Previous examples have used Python functions, but we haven't defined any ourselves, yet.
# Functions allow us to reuse code that otherwise would be repeated in different parts
# of our program. This has multiple benefits:
#
# - Any problems in a function would only need to be fixed once, instead of multiple places.
# - Shorter, reusable functions can be more easily understood and tested than longer blocks of code.

# This function computes the sum of items in a container.
def sum(lst):
    result = 0
    for x in lst:
        result += x
    return result


# Test out the sum function:
print()
print('sum([1, 2, 3, 4]) = ', sum([1, 2, 3, 4]))
print('sum([-1, 0, 0.5, 0.5]) = ', sum([-1, 0, 0.5, 0.5]))


# Python allows you to define functions anywhere in the code. Here are a few more functions;
# can you figure out what they do?

def average(lst):
    size = len(lst)
    return sum(lst) / size


def message(lst):
    return 'avg(' + str(lst) + ') = '


def print_average(lst):
    avg = average(lst)
    print(message(lst) + str(avg))


numbers = [5, 10, 15, -5, 0]

print()
print_average(numbers)
numbers.append(0)
numbers.append(0)
print_average(numbers)
numbers.append(100)
print_average(numbers)

empty_list = []
# print_average(empty_list)  # 📛 Error!
