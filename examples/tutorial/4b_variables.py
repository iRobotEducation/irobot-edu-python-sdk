#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

# Python allows to assign multiple variables in the same line:
x, y, z = 100, 200, 300
print('x, y, z =', x, y, z)

# Even if they are of different data types:
v, w, x, y, z = False, 'Hi!', 'Bye', 300, 0.5
print('w, x, y, z =', w, x, y, z)

print()
print('Classic swap:')

# Let's swap the values of two variables
# (in the way it's commonly done in other programming languages)
a = 10
b = 9
print('a, b =', a, b)

# The values bound with "a" and with "b" are immutable (integer) objects.
# (We will learn more about immutable and mutalbe ojbects in the Container lessons.)
temp = a  # temp is now 10.
a = b  # a is now 9, but temp WILL NOT be affected.
b = temp
print('a, b =', a, b)

# Now, with what we learned about Python multiple assignments in a single line...
print()
print("Python's swap without a temp variable!")

a = 100
b = 'Hello!'
print('a, b =', a, b)

a, b = b, a
print('a, b =', a, b)
