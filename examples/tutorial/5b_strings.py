#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

# Python has really powerful text/string manipulation capabilities. Here are a few examples.
# You can learn more at https://docs.python.org/3/tutorial/introduction.html#strings

print()
text = 'Python also offers ways to manipulate strings, and to access substrings and characters:'
print('text =', text)
print()
print('len(text) --> ', len(text))
print('text[0] --> ', text[0])  # Accessing individual characters; in this case, the one at position 0.
print()
print("Let's experiment with Python's string slices:")
print('text[0:6] --> ', text[0:6])  # Returns the characters from position 0 (included) to 5 (excludes 6).
print('text[:] --> ', text[:])  # Omitting the start and stop indexes, will return the whole original string.
print('text[5:11] --> ', text[5:11])
print('text[5:11:2] --> ', text[5:11:2])  # The "2" value here is the step: so it will skip some letters!
print('text[11:5:-1] --> ', text[11:5:-1])  # The "-1" step value can be used to reverse slices.
print('text[::-1] --> ', text[::-1])  # Reverses the whole string!
print('text[-11:] --> ', text[-11:])  # This returns the 11 last characters of the string.

print()
print("Combining string slices with the string's find method:")
print('text[text.find("also"):text.find("manipulate")] --> ', text[text.find("also"):text.find("manipulate")])
