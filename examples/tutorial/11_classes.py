#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

# Classes are an important concept in some Object Oriented Programming languages. Python is one of those.

class BasicRobot:
    # Every function belonging to a class is a method.
    # Every method receives the 'self' parameter, which will not be explicitly passed once the method is called.
    def __init__(self, name):
        self.name = name  # The parameter "name" is stored in the property "self.name".
        print('A BasicRobot named "' + self.name + '" was instantiated')

    def move(self, distance):
        print('moving', str(distance) + '(cm)')

    def turn_left(self, angle):
        print('turning left', str(angle) + '(deg)')

    def turn_right(self, angle):
        print('turning right', str(angle) + '(deg)')


print()
print('Creates a BasicRobot instance:')
print()

br = BasicRobot('Create 3')
print('br.name =', br.name)
br.move(16)
br.turn_left(90)
br.turn_right(45)

print()
print('Classes can inherit from other classes')
print()


class Root(BasicRobot):
    def __init__(self, name):
        super().__init__(name)  # Calls the __init__ method of the super class.
        print('Root robots also have a marker!')

    def marker_down(self):
        print('Marker is down')

    def marker_up(self):
        print('Marker is up')


root0 = Root('root0')
print()
root1 = Root('root1')

print()
root0.move(-16)
root1.marker_up()
root1.marker_down()
