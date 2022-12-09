#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

# Loops give us ways to repeat actions or to perform iterations.

print()
distance = 0
while distance < 3:
    distance += 1  # Same as: distance = distance + 1
    print('distance = ' + str(distance) + ' cm')

print()
txt = 'Useful experimental string'
print(txt)

# In Python, variables can be defined anywhere.
# Previously, we have assigned variables on their own lines as an atomic action.
# But it is possible to create a variable in the middle of another function, as well.
# Here, we create the variable 'i' as a loop iterator:
for i in txt:
    print(i)
    if i == 'l':
        break

print()
print('Loops can be nested:')
count = 3
while count > 0:
    another_txt = ''
    for i in txt[7:]:
        if i == 'a':
            break
        another_txt += i
    count -= 1  # Same as count = count - 1
    print(another_txt + ' ' + str(count))
