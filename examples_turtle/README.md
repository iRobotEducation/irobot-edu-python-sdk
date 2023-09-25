# Turtle interface for the iRobot® Education Python® SDK

This portion of the SDK implements an alternative interface to the SDK following the paradigm of 
[turtle graphics](https://en.wikipedia.org/wiki/Turtle_graphics).
It provides a limited, simplified, and synchronous interface to the in the spirit (and largely the syntax) of the 
[Python® turtle.Turtle class](https://docs.python.org/3/library/turtle.html).
It can be used on any robot supported by the SDK, using any supported backend.

## Disclaimer: this is part of the ALPHA release

This new feature is provided "as is" to conduct testing and gather user feedback. We hope this feature is useful and
welcome feedback and suggestions for improvement.

## Usage

This module is a work-alike (albeit not a direct drop-in replacement) for movement and control using conventional
Turtle-like commands, such as the following:

* `forward(8)`
* `right(90)`
* `pendown()`

and others. These commands are naturally mapped onto the corresponding movement functions supported by the educational
robots.

To create an object that will control the robot with Turtle commands, the following pattern can be used:

```Python
backend = Bluetooth('ROBOT_NAME')
robot = Robot(backend)
rt = RobotTurtle(robot)
```

This will attempt to connect to the specified robot via Bluetooth® Low Energy (leave the `Bluetooth()` argument blank
to connect to the first detected supported robot device). After that, create a RobotTurtle handle for it. The
RobotTurtle constructor will block until connected. After it is connected, the RobotTurtle object
(in this example, called `rt`) can be directed to perform actions using Turtle commands, such as

```Python
rt.forward(8)
rt.right(90)
rt.pendown()
```

These commands will be sent to the robot one at a time, and will direct the robot to move forward 8 cm, then rotate
(in place) 90 degrees to the right, then put the marker down (for robots that support a drawing pen). Each command will
run to completion before the statement returns.

### Limitations

Due to the synchronous, explicit, and imperitive programming model of Turtle, it is not possible to use some more
advanced features of this SDK. For example, there is no direct way to use the Turtle model to program a custom response
to a particular event, such as bumper contact.

## Modes of operation

The RobotTurtle can be used as a script or can be used interactively as a REPL (Read, Execute, Print, Loop).

### REPL example

The file `robot_turtle_init_repl.py` is a simple example to allow direct REPL-style interaction with the robot. It
should be started in "interactive" mode, such as

```commandline
python3 -i robot_turtle_init_repl.py
```

The script will automatically attempt to connect to a robot and then display some helpful information. After the robot
is connected, it will display a `>>>` prompt and you can type Turtle commands to the robot using the `rt` object, such
as those listed above. An explicit device name is accepted, such as 

```commandline
python3 -i robot_turtle_init_repl.py --bluetooth ROBOT_NAME
```

Once the robot is connected, you will be offered an informational message. You may execute REPL-style interactive
commands at the `>>> ` prompt, using the Turtle-style interface, on the object called `rt`, such as the following:

```
>>> rt.forward(8)
>>> rt.right(90)
```

As usual, the specified function will block until the action is complete.
More information can be found in the sources or by running in non-interactive mode with the `--help` argument:

```commandline
python3 robot_turtle_init_repl.py --help
```

### Script examples

The file `robot_turtle_draw_polygon.py` is a simple example that illustrates basic usage of this library. It will draw
a simple regular polygon based on the constants in the file. By default, it will draw a regular pentagon with 16 cm
sides. Use command-line arguments or edit the constants `NUM_SIDES` and `EDGE_LENGTH` in the file to draw polygons of
other proportions, or use it as a reference for your own movements! See `--help` for more information.

The file `robot_turtle_example.py` illustrates other options for using the library, including other interfaces and
use of robot-specific classes in case you want to use special features of a specific robot. It includes a verbose
command-line interface as a means of illustrating some more features of this implementation of the Turtle model.
It also allows the use of `python -i robot_turtle_example.py` for interactive mode.


## Currently-supported operations

The following Turtle operations are currently supported (aliases listed in parentheses):

Movement:

* forward (fd)
* backward (bk, back)
* right (rt)
* left (lt)
* goto (setpos, setposition)
* setx
* sety
* setheading (seth)
* home
* circle
* dot

State:

* position (pos)
* xcor
* ycor
* heading
* distance

Pen control:

* pendown (pd, down)
* penup (pu, up)
* isdown()

Miscellaneous and non-Turtle operations:

* mode
* sleep (wait)

