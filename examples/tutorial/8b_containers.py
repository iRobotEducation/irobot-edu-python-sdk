#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

# Nested containers.

print('list of lists:')
tic_tac_toe = [
    ['X', 'O', 'O'],
    ['O', 'X', 'O'],
    ['O', 'O', 'X'],
]
print(tic_tac_toe)
print()

print('Nicer printing:')
for row in tic_tac_toe:  # row can have any name.
    print(row)  # Each "row" is a list inside the tic_tac_toe list.


print()
print('Different types of containers can be nested:')

robots = [  # List of robots with dictionaries of sensors and their values.
    {
        'distance_sensor': 10,
        'cliff_sensor': True,
        'battery_sensor': 12.6,
    },
    {
        'distance_sensor': 8,
        'cliff_sensor': False,
        'battery_sensor': 8.9,
    },
]

# print(robots)
print()

i = 0
while i < len(robots):
    battery_level = robots[i]['battery_sensor']
    if battery_level < 10:
        print('Robot number', i, 'needs to charge (battery level =', battery_level, 'V)')
    i += 1
