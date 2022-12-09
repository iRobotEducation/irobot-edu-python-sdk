#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

# In software engineering, a "string" is a data type representing zero or more characters.
# Let's start learning about how strings work in Python.

print()
print('We were already using strings as print() arguments in previous examples.')
str1 = 'We also used string variables'
str2 = str1 + ', which can be combined like this.'
print(str2)
print('Strings and numbers can also work together: ' + str(3.141592))
# print('Strings and numbers can also work together: ' + 3.141592)  # 📛 Error!

print()
print('Using "" inside a string')
print("Using '' inside a string")
print()

text = 'Python also offers ways to manipulate the strings, and to access substrings and characters:'
print('text =', text)

print()
print('Finding substrings ("-1" means that the substring was not found in the original string):')
print('text.find("Python") --> ', text.find("Python"))
print('text.find("python") --> ', text.find("python"))
print('text.find("also") --> ', text.find("also"))

print()
