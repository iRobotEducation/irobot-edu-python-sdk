#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2023 iRobot Corporation. All rights reserved.
#

# Let's see what Python's containers can do for our programs.

print()
print('Lists:')
robots = ['Root', 'Create 3', 'Roomba']
print(robots)

# A "for" loop in Python allows our program to iterate over the content of a container:
for n in robots:
    print(n)

print()
j = 0
while j < len(robots) - 1:
    print(robots[j] + ' is a friend of ' + robots[j + 1])
    j += 1

print()

# In Python, lists are objects, which can have methods. "Methods" are a name for functions attached to objects.
# "sort()" is one such inbuilt method, which will arrange the elements in ascending order depending on their type.
# We will learn more about methods soon, in the lesson about "Classes"...
robots.sort()
print(robots)

print('Adding some elements:')
robots.append('Root')  # "append", like "sort", is also a list method.
robots.append('Roomba')
print(robots)

print()
print('Sets store only unique elements:')
s = set(robots)  # This creates a set from the "robots" list.
print(s)
print("'root' in s --> ", 'root' in s)
print("'Root' in s --> ", 'Root' in s)

print()
print('Dictionaries allow us to add a key to find elements:')
inventory = {
    'Root': 512,
    'Roomba': 1024,
    'Create': 128
}

print("inventory['Root'] --> ", inventory['Root'])
print("inventory['Roomba'] --> ", inventory['Roomba'])
# print("inventory['Root'] --> ", inventory['root'])  # 📛 Error!
print("'root' in inventory --> ", 'root' in inventory)  # Do this instead to find out if the key is present in the dictionary.

print()
print('You may also want to search the Internet for "Python tuples."')
