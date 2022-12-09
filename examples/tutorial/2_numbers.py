#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

# There are 3 types of numbers in Python: integer, floating point and complex.
# But we won't deal with complex numbers in this tutorial.

print()  # Blank line.
print('Integer numbers:')
print('print(3)  --> ', 3)
print('print(int(3.0))  --> ', int(3.0))

print()
print('Floating point numbers:')
print('(you can learn more about them at https://docs.python.org/3/tutorial/floatingpoint.html)')
print('print(3.0)  --> ', 3.0)
print('print(float(3))  --> ', float(3))

print()
print('Some comparison operators:')
print('print(3 == 3.0) --> ', 3 == 3.0)
print('print(-1 < 0) --> ', -1 < 0)
print()
print('Be careful when comparing floating point numbers! 😉')
print('It is a better practice to use comparison operators such as <=, <, >, >=')
print('print(2.1 + 2.2) --> ', 2.1 + 2.2)
print('print(2.1 + 2.2 == 4.3) --> ', 2.1 + 2.2 == 4.3)  # ❌ False
print('print(3.1 + 3.1) --> ', 3.1 + 3.1)
print('print(3.1 + 3.1 == 6.2) --> ', 3.1 + 3.1 == 6.2)

print()
print('print(pow(3, 2)) --> ', pow(3, 2))
