#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

# In Python, there is a huge difference between mutable and immutable types.
# Let's see how each of those work.

# Most Python built-in types are immutable.
# This means that their values can't be changed after the object was created.
# Let's see some examples...

# The "x" name is now bound to the the immutable integer object whose value is 3.14:
x = 3.14

# The "y" name is now bound to the the immutable integer object whose value is 3.14:
y = x

print('x, y =', x, y)

# That means that modifying one of then, DOES NOT modify the other one:
x = 2.71
print('x, y =', x, y)

# The same can be done with strings, booleans, and a bunch of other types...
x = 'Flying robot'
y = x
print('x, y =', x, y)
x = 'Walking robot'
print('x, y =', x, y)
print()

# But a few types (such as lists, dictionaries and sets) are MUTABLE.
# For these, changing one variable referencing that object, changes ALL of them:
x = ['Roomba', 'Root', 'Create 3']  # List
y = x
print('x =', x)
print('y =', y)
print()
y.sort()  # We are modifying both here!
print('x =', x)
print('y =', y)
print()

# But, what if we want to reallly make a COPY a list, in a way that the 2 references are now independent?
# One way of doing it Python is like this:

list0 = [1, 2, 8, 16]
list1 = list(list0)  # This creates a COPY of list0, referenced by list1
print('list0 =', list0)
print('list1 =', list1)
print()
list0.append(32)
list1.append(128)
print('list0 =', list0)
print('list1 =', list1)
print()
print('Can you find out how to do the same for other mutable types?')
