#!/usr/bin/env python3
#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2023 iRobot Corporation. All rights reserved.
#

import asyncio
import functools
import logging
import math
import queue
import threading

from .robots import event, Robot, Root, Create3
from .getter_types import Pose, Movement


# TODO:
# [ ] Use getter function for Marker state? or ignore support?
# [ ] Wait until after connected to return, instead of turtlerobot.sleep(0)?
# [ ] Support radians mode
# [ ] Support `towards()` function

# NOTES:
# Concept of operation:
# * Upon initialization, the constructor creates several resources:
#   => a (thread-safe) queue.Queue;
#   => a Robot object from provided Backend;
#   => a (separate) worker thread
# * the main event loop (Robot.play()) is executed in the worker thread
# * the worker thread loops, blocking each loop on reading from the queue
# * the main thread enqueues actions into the queue
# * Actions must be callable objects,
#   intended to be functools.partial that wraps an async def robot action with all arguments

# A few default items differ from conventional / classic Turtle definitions or behavior:
# * default "mode" is not quite any of the defaults:
#   => "mode" is defined as "standard": positive angles are counterclockwise
#   => initial heading is defined as 90 degrees, canonically "to the right", but in "standard" mode this is 0 degrees
# * pen is up (not down) by default

# Author's note: I wish this could be a proper subclass of the Python standard library turtle.Turtle class.
# Upon some consideration I was not able to find a way (that I believed to be satisfactory) to graft this into the
# very graphics-/screen-oriented nature of turtle.Turtle. This is an entirely separate, albeit work-alike,
# implementation.

class RobotTurtle:
    """turtle.Turtle-like interface for iRobot EDU interface."""
    # TODO: consider if this could actually be a subclass of turtle.Turtle
    # The mechanics of adapting physical control to a graphics drawing canvas are daunting.
    # The resulting (unused) dependency on a Tk-like drawing library doesn't feel quite right either.

    VERSION = '0.5.2'

    def __init__(self, robot: Robot, queue_depth=1, log_level=logging.INFO):
        """
        Initialize a Robot or FakeRoot to service commands.
        Create a thread-safe queue for directions.
        Fork a worker thread to service Robot's asyncio loop while allowing parallel interaction.
        To maintain consistent with the "synchronous" behavior of this module, this constructor will block until
        connected to the robot (it will return after connection to robot is successful).
        :param robot: irobot_edu_sdk.robots.Robot (e.g., RootRobot) or None (FakeRobot)
        :param queue_depth: depth of dispatch queue; 1 is synchronous/blocking; !=1 untested
        """
        # TODO: consider adding FakeRobot or providing error handling/message
        self._robot = robot  # if robot else FakeRobot()
        # TODO: state that might should be stored elsewhere, like robot object...
        self._mode = 'standard'  # imprecise; see notes above and Python Turtle documentation for more
        self._marker_state = Root.MarkerPos.UP
        # Note: as of this writing only the Root has a `pose` field; duplicate here;
        if hasattr(self._robot, 'pose'):
            self._pose = self._robot.pose
        else:
            self._pose = Pose()

        # Management fields
        self._logger = logging.getLogger('asyncio.RobotTurtle')
        self._logger.setLevel(log_level)
        # Queue depth==1 results in blocking behavior of the Turtle interface
        # >1 results in immediate-issue queue behavior
        self._thread_queue = queue.Queue(queue_depth)
        self._worker_thread = threading.Thread(target=self._thread_worker, daemon=True)
        self._worker_thread.start()

        # This construct is necessary to provide a function that matches the signature needed for when_play,
        # but lacks a "self" object argument (i.e., an instance function cannot be decorated with when_play event)
        # I don't think a static function would work since it needs to encapsulate references within `self`.
        # I'm interested to hear alternatives that seem a little more common-looking.
        @event(self._robot.when_play)
        async def _asyncio_worker_wrap(worker_robot):
            await self._asyncio_worker(worker_robot)

        self.wait(0)  # block until asynchronous connection is established

    # Enable clean exit
    def stop(self):
        """Attempt a disconnect from the robot"""
        self._logger.warning('Disconnecting from Robot...')
        self._enqueue_action(self._robot._finished)

    # For robots that do NOT natively support `pose`, optimistically update pose based on planned movement
    # For robots that natively support `pose`, do nothing (it is done implicitly by movement commands)
    def _maybe_update_pose_move(self, distance):
        if not hasattr(self._robot, 'pose'):
            self._pose.move(distance)

    def _maybe_update_pose_location(self, new_x = None, new_y = None):
        if not hasattr(self._robot, 'pose'):
            # If argument passed is None, do not update that dimension
            if new_x is not None:
                self._pose.x = new_x
            if new_y is not None:
                self._pose.y = new_y

    def _maybe_update_pose_turn_left(self, angle):
        if not hasattr(self._robot, 'pose'):
            self._pose.turn_left(angle)

    def _maybe_update_pose_heading(self, angle):
        if not hasattr(self._robot, 'pose'):
            self._pose.heading = angle

    def _thread_worker(self):
        """threading.Thread worker; runs the Robot asyncio loop"""
        self._logger.debug('thread-worker about to robot-play...')
        self._robot.play()
        self._logger.debug('thread-worker completed play...?')

    async def _get_ts_queue(self):
        """async wrapper for a synchronous interface to thread-safe queue.Queue (not asyncio.queue)"""
        while True:
            try:
                action = self._thread_queue.get_nowait()
                return action
            except queue.Empty:
                await asyncio.sleep(0.1)  # Throttle? notsureif

    async def _asyncio_worker(self, robot):
        """The async worker Task for receiving and dispatching actions to Robot
        Block on incoming queue for actions (expected to be an awaitable functools.partial)
        Await the action, then signal the Queue.
        """
        action_number_ordinal = 0
        while True:
            self._logger.debug('a-worker about to await queue-get')
            # Get a "work item" out of the queue.
            action = await self._get_ts_queue()
            self._logger.debug('a-worker got queue get: %s', action)

            # Dispatch an `await action()`
            await action()

            # Notify the queue that the "work item" has been processed.
            self._thread_queue.task_done()

            self._logger.debug('a-worker completed action %d', action_number_ordinal)
            action_number_ordinal += 1

    def _enqueue_action(self, action, *args):
        """Helper function to enqueue the specified async def action, with optional, variable argument list,
        then block/wait until completion ("join" the queue)"""
        self._thread_queue.put(functools.partial(action, *args))
        self._thread_queue.join()

    # The turtle.Turtle-like interface to this class.
    # Interface derived from https://docs.python.org/3/library/turtle.html
    # Note that many of these functions have built-in shortened form or aliases

    # Move/draw and pen control
    def mode(self, new_mode=None):
        """Stub of Turtle mode operation; only default mode currently supported"""
        # If no argument or None, return current mode
        if new_mode is None:
            return self._mode
        elif new_mode == self._mode:
            return
        else:
            self._logger.error('Mode not set: mode %s not implemented')

    """Sleep for specified time"""
    def wait(self, seconds=0.0):
        self._enqueue_action(asyncio.sleep, seconds)

    sleep = wait

    # Movement functions are synchronous and can be called interactively or from main().
    # Blocks until complete due to queue.join()

    # Put the pen down. Note well: Turtle has the equivalent of Root.MarkerPos.DOWN by default, but Root doesn't
    # This has no effect on robots without Pen, such as Create3
    def pendown(self):
        """Set the robot pen to the down (marking) position. Only supported on some robot families."""
        if hasattr(self._robot, 'set_marker'):
            self._enqueue_action(self._robot.set_marker, Root.MarkerPos.DOWN)
            # Store new state locally as a field. TODO: replace with getter function from actual robot object.
            self._marker_state = Root.MarkerPos.DOWN
        else:
            self._logger.debug('Robot %s has no set_marker support; ignoring request', self._robot.__class__.__name__)

    pd = down = pendown

    # Raise the pen up.
    def penup(self):
        """Set the robot pen to the up (non-marking) position. Only supported on some robot families."""
        if hasattr(self._robot, 'set_marker'):
            self._enqueue_action(self._robot.set_marker, Root.MarkerPos.UP)
            # Store new state locally as a field. TODO: replace with getter function from actual robot object.
            self._marker_state = Root.MarkerPos.UP
        else:
            self._logger.debug('Robot %s has no set_marker support; ignoring request', self._robot.__class__.__name__)

    pu = up = penup

    # Make a dot at the current location
    def dot(self):
        # If the marker is already down, `dot()` should do nothing
        if self._marker_state == Root.MarkerPos.DOWN:
            return
        else:
            self.pendown()
            self.penup()

    # TODO: need getter function from actual Robot object
    def isdown(self):
        """Return a boolean representing whether the marker is down (True) or up (False)"""
        return self._marker_state == Root.MarkerPos.DOWN

    def forward(self, centimeters):
        """Command the robot to move forward by specified distance in cm."""
        self._enqueue_action(self._robot.move, centimeters)
        self._maybe_update_pose_move(centimeters)

    fd = forward

    def backward(self, centimeters):
        """Command the robot to move backward by specified distance in cm."""
        self._enqueue_action(self._robot.move, -centimeters)
        self._maybe_update_pose_move(-centimeters)

    bk = back = backward

    def right(self, degrees):
        """Command the robot to turn right (clockwise) by specified angle, in degrees."""
        self._enqueue_action(self._robot.turn_right, degrees)
        self._maybe_update_pose_turn_left(-degrees)

    rt = right

    def left(self, degrees):
        """Command the robot to turn left (counter-clockwise) by specified angle, in degrees."""
        self._enqueue_action(self._robot.turn_left, degrees)
        self._maybe_update_pose_turn_left(degrees)

    lt = left

    def turn(self, degrees, direction):
        """Command the robot to turn in the specified amount in the specified direction, in degrees.
           Direction should be one of Robot.Dir.LEFT or Robot.Dir.RIGHT"""
        if direction == Robot.Dir.LEFT:
            self._enqueue_action(self._robot.turn_left, degrees)
            self._maybe_update_pose_turn_left(degrees)
        elif direction == Robot.Dir.RIGHT:
            self._enqueue_action(self._robot.turn_right, degrees)
            self._maybe_update_pose_turn_left(-degrees)
        else:
            self._logger.error('turn() direction should be Robot.Dir.LEFT or Robot.Dir.RIGHT; got %s', direction)
            return

    def circle(self, radius, extent=360, steps=None):
        """Command the robot to move in an arc of a circle with specified radius in cm.
           Positive radius results in an arc curving to the left; negative radius arcs to the right.
           Extent is the degrees of the arc, where 360 (default) is a full circle."""
        # Author's note: the Turtle interface defines extent default as None to draw a full (360º) circle
        #                In this implementation, 360 is chosen as default to be explicit.
        # TODO: support "steps" argument by manually walking an inscribed polygon
        # Note well: Robot sense is arc clockwise; here it is inverted to be consistent with angles and Turtle
        if not radius:
            self._logger.error('circle() radius must be not be 0')
            return
        elif radius > 0:
            direction = Robot.Dir.LEFT
        else:
            direction = Robot.Dir.RIGHT
        if extent is None:
            extent = 360
        if extent <= 0:
            self._logger.error('circle() extent must be > 0')
            return
        if steps is None:
            # Draw a proper circle.
            self._enqueue_action(self._robot.arc, direction, extent, abs(radius))
        else:
            # Draw an inscribed regular polygon by steps.
            # Use N steps no matter if extent is full circle (360 degrees) or not.
            # Adapted from https://math.stackexchange.com/questions/1712375/perimeter-and-area-of-a-regular-n-gon
            edge_len = 2 * abs(radius) * math.sin(math.pi / steps * extent / 360)
            turn_degrees = extent / steps
            self._logger.error('circle(): turning total %s degrees in %s steps of %s cm at angle of %s to the %s',
                               extent, steps, edge_len, turn_degrees, 'right' if direction == Robot.Dir.RIGHT else 'left')
            for ii in range(steps):
                self.forward(edge_len)
                self.turn(turn_degrees, direction)

    # By convention, heading is preserved by this function; retain that behavior here
    def goto(self, x, y):
        """Command the robot to navigate to specified absolute location.
           As with Turtle, heading is restored after movement."""
        # TODO: allow x to be a Vec2D or a single argument as a 2-tuple?
        # Note: Both dimensions required; use setx() or sety() for single dimension
        # Note: the behavior of this function using the graphics library retains heading; Robot does not
        #   e.g., if turtle is facing RIGHT at (0, 0) then commanded to goto(0, 8):
        #   Turtle would end up still facing RIGHT (translated but retaining original heading)
        #   Robot would turn, then move, and end up facing UP, so must be instructed to restore original heading
        # Record original heading to restore later
        original_heading = self._pose.heading
        self._logger.debug('Starting at heading %s', original_heading)
        # N.B.: Looks like Root::navigate_to does not handle heading properly; bug?
        # WOULD BE: self._thread_queue.put(functools.partial(self._robot.navigate_to, x, y, original_heading))
        self._enqueue_action(self._robot.navigate_to, x, y)
        # Restore original heading
        self._enqueue_action(self._robot.turn_left, Movement.minimize_angle(original_heading - self._pose.heading))
        self._maybe_update_pose_location(x, y)

    setpos = setposition = goto

    # Go back to 0, 0 location
    def home(self):
        self.goto(0, 0)

    def setx(self, x):
        """As with goto() but only change X coordinate."""
        self.goto(x, None)
        self._maybe_update_pose_location(new_x=x)

    def sety(self, y):
        """As with goto() but only change Y coordinate."""
        self.goto(None, y)
        self._maybe_update_pose_location(new_y=y)

    def setheading(self, angle):
        """Adjust the robot heading to the specified absolute heading."""
        self._enqueue_action(self._robot.turn_left, Movement.minimize_angle(angle - self._pose.heading))
        self._maybe_update_pose_heading(angle)

    seth = setheading

    # Tell Turtle's State
    def position(self):
        """Return location as a 2-tuple of X, Y coordinates."""
        return self._pose.x, self._pose.y

    pos = position

    def xcor(self):
        """Return X component of robot location."""
        return self._pose.x

    def ycor(self):
        """Return Y component of robot location."""
        return self._pose.y

    def heading(self):
        """Return robot heading in degrees."""
        return self._pose.heading
