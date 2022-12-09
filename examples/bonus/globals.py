#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

a = 11.2
b = -4

temp = a
a = b
b = temp

print(a, b, temp)
print()

# Creates a copy of the dictionary that implements the current module namespace:
g = dict(globals())

# Iterates over that dictionary: the variables defined above will be there.
# Also, note the (k, v) construction to iterate over the dictionary's key-value pairs.
for (k, v) in g.items():
    print((k, v))
