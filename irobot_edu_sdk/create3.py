#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2024 iRobot Corporation. All rights reserved.
#

import math
from enum import IntEnum, IntFlag
from typing import Union, Callable, Awaitable, List, Tuple, Optional
from struct import pack, unpack
from dataclasses import dataclass
from .backend.backend import Backend
from .event import Event
from .completer import Completer
from .packet import Packet
from .utils import bound
from .getter_types import IPv4Addresses, IrProximity, Pose, DockingSensor
from .robot import Robot

@dataclass
class Waypoint:
    """Represents a navigation waypoint with position and optional heading"""
    x: float
    y: float
    heading: Optional[float] = None
    tolerance: float = 5.0  # cm
    heading_tolerance: float = 5.0  # degrees

@dataclass
class NavigationState:
    """Represents the current state of navigation"""
    current_waypoint: Optional[Waypoint] = None
    waypoints: List[Waypoint] = None
    is_navigating: bool = False
    obstacle_detected: bool = False
    last_obstacle_position: Optional[Tuple[float, float]] = None

class Create3(Robot):
    """Create 3 robot object."""

    class DockStatus(IntEnum):
        SUCCEEDED = 0
        ABORTED   = 1
        CANCELED  = 2

    class DockResult(IntEnum):
        UNDOCKED = 0
        DOCKED   = 1

    class DockSensorEnum(IntEnum):
        """Enum for docking sensor states"""
        NO_CONTACT = 0
        CONTACT = 1
        IR_SENSOR_0 = 2
        IR_SENSOR_1 = 3
        IR_SENSOR_2 = 4

    def __init__(self, backend: Backend):
        super().__init__(backend=backend)

        self._events[(19, 0)] = self._when_docking_sensor_handler

        self._when_docking_sensor: list[Event] = []
        self._docking_sensor_triggers: dict[DockSensorEnum, list[Event]] = {
            self.DockSensorEnum.NO_CONTACT: [],
            self.DockSensorEnum.CONTACT: [],
            self.DockSensorEnum.IR_SENSOR_0: [],
            self.DockSensorEnum.IR_SENSOR_1: [],
            self.DockSensorEnum.IR_SENSOR_2: []
        }

        # Getters.
        self.ipv4_address = IPv4Addresses()
        self.docking_sensor = DockingSensor()

        # Use Create 3 robot's internal position estimate
        self.USE_ROBOT_POSE = True

        # Navigation state
        self._navigation_state = NavigationState()
        self._navigation_state.waypoints = []
        
        # Navigation parameters
        self.OBSTACLE_DETECTION_THRESHOLD = 30  # cm
        self.OBSTACLE_AVOIDANCE_DISTANCE = 50  # cm
        self.NAVIGATION_SPEED = 0.5  # m/s

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    # Event Handlers.

    async def _when_docking_sensor_handler(self, packet):
        if len(packet.payload) > 4:
            # Update cached values
            self.docking_sensor.contacts = packet.payload[4] != 0
            self.docking_sensor.sensors = (packet.payload[5],
                                         packet.payload[6],
                                         packet.payload[7])

            # Trigger general docking sensor event
            for event in self._when_docking_sensor:
                await event.run(self)

            # Trigger specific sensor events
            if self.docking_sensor.contacts:
                for event in self._docking_sensor_triggers[self.DockSensorEnum.CONTACT]:
                    await event.run(self)
            else:
                for event in self._docking_sensor_triggers[self.DockSensorEnum.NO_CONTACT]:
                    await event.run(self)

            # Trigger IR sensor events
            for i, sensor_value in enumerate(self.docking_sensor.sensors):
                if sensor_value > 0:  # Assuming 0 means no detection
                    for event in self._docking_sensor_triggers[self.DockSensorEnum(i + 2)]:
                        await event.run(self)

    # Event Callbacks.

    def when_docking_sensor(self, callback: Callable[[bool], Awaitable[None]]):
        """Register a callback for any docking sensor event"""
        self._when_docking_sensor.append(Event(True, callback))

    def when_docking_sensor_trigger(self, trigger: DockSensorEnum, callback: Callable[[bool], Awaitable[None]]):
        """Register a callback for a specific docking sensor trigger"""
        self._docking_sensor_triggers[trigger].append(Event(True, callback))

    # Commands.

    async def get_ipv4_address(self) -> IPv4Addresses:
        """Get the robot's ipv4 address as a IPv4Addresses, which contains wlan0, wlan1 and usb0. Returns None if anything went wrong."""
        dev, cmd, inc = 100, 1, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        if packet:
            self.ipv4_address.wlan0 = [packet.payload[0], packet.payload[1], packet.payload[2], packet.payload[3]]
            self.ipv4_address.wlan1 = [packet.payload[4], packet.payload[5], packet.payload[6], packet.payload[7]]
            self.ipv4_address.usb0 = [packet.payload[8], packet.payload[9], packet.payload[10], packet.payload[11]]
            return self.ipv4_address
        return None

    async def get_6x_ir_proximity(self):
        """Get Original IR Proximity Values and States"""
        dev, cmd, inc = 11, 1, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        if packet:
            unpacked = unpack('>IHHHHHH', packet.payload)
            ir_proximity = IrProximity()
            ir_proximity.sensors = list(unpacked[1:])
            return ir_proximity
        return None

    async def get_packed_ir_proximity(self):
        """DEPRECATED function for new Get IR Proximity Values and States"""
        print('Warning: get_packed_ir_proximity() has been deprecated, please use get_ir_proximity() instead')
        await self.get_7x_ir_proximity()

    async def get_7x_ir_proximity(self):
        """Get Packed IR Proximity Values and States"""
        dev, cmd, inc = 11, 2, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        if packet:
            payload = packet.payload
            timestamp = unpack('>I', payload[0:4])[0]
            ir_proximity = IrProximity()
            #ir_proximity.state = payload[4]
            ir_proximity.sensors = [
                (payload[ 5] << 4) + (payload[12] >> 4),
                (payload[ 6] << 4) + (payload[12] & 0xF),
                (payload[ 7] << 4) + (payload[13] >> 4),
                (payload[ 8] << 4) + (payload[13] & 0xF),
                (payload[ 9] << 4) + (payload[14] >> 4),
                (payload[10] << 4) + (payload[14] & 0xF),
                (payload[11] << 4) + (payload[15] >> 4),
            ]
            return ir_proximity
        return None

    async def get_ir_proximity(self):
        """Version-Agnostic Get IR Proximity Values and States"""
        ir_prox = await self.get_7x_ir_proximity()
        if ir_prox is not None:
            return ir_prox

        ir_prox = await self.get_6x_ir_proximity()
        if ir_prox is not None:
            print('Warning: ir_prox() missing seventh value; you may need to update your robot')
            ir_prox.sensors.append(float('nan'))
            return ir_prox

        return None

    async def navigate_to(self, x: Union[int, float], y: Union[int, float], heading: Union[int, float] = None):
        """ If heading is None, then it will be ignored, and the robot will arrive to its destination
        pointing towards the direction of the line between the destination and the origin points.
        Units:
            x, y: cm
            heading: deg
        """

        if self._disable_motors:
            return
        dev, cmd, inc = 1, 17, self.inc
        _heading = -1
        if heading is not None:
            _heading = int(heading * 10)
            _heading = bound(_heading, 0, 3599)
        payload = pack('>iih', int(x * 10), int(y * 10), _heading)
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc, payload))
        
        dx = x - self.pose.x
        dy = y - self.pose.y
        timeout = self.DEFAULT_TIMEOUT + int(math.sqrt(dx * dx + dy * dy) / 10) + 4  # 4 is the timeout for a potential rotation.
        
        packet = await completer.wait(timeout)
        if self.USE_ROBOT_POSE and packet:
            return self.pose.set_from_packet(packet)
        else:
            if heading is not None:
                self.pose.set(x, y, heading)
            else:
                self.pose.set(x, y, math.degrees(math.atan2(y - self.pose.y, x - self.pose.x)) + self.pose.heading)

            return self.pose

    async def dock(self):
        """Request a docking action."""
        dev, cmd, inc = 1, 19, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(60)
        if packet:
            unpacked = unpack('>IBBHHHHH', packet.payload)
            return {'timestamp': unpacked[0], 'status': self.DockStatus(unpacked[1]), 'result': self.DockResult(unpacked[2])}
        return None

    async def undock(self):
        """Request an undocking action."""
        dev, cmd, inc = 1, 20, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(30)
        if packet:
            unpacked = unpack('>IBBHHHHH', packet.payload)
            return {'timestamp': unpacked[0], 'status': self.DockStatus(unpacked[1]), 'result': self.DockResult(unpacked[2])}
        return None

    async def get_docking_values(self):
        """Get docking values. Returns cached values if available, otherwise fetches from robot."""
        # Return cached values if available
        if hasattr(self.docking_sensor, 'contacts') and hasattr(self.docking_sensor, 'sensors'):
            return {
                'timestamp': 0,  # We don't have timestamp in cached values
                'contacts': self.docking_sensor.contacts,
                'IR sensor 0': self.docking_sensor.sensors[0],
                'IR sensor 1': self.docking_sensor.sensors[1],
                'IR sensor 2': self.docking_sensor.sensors[2]
            }

        # If no cached values, fetch from robot
        dev, cmd, inc = 19, 1, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        if packet:
            unpacked = unpack('>IBBBBHHHH', packet.payload)
            return {
                'timestamp': unpacked[0],
                'contacts': unpacked[1],
                'IR sensor 0': unpacked[2],
                'IR sensor 1': unpacked[3],
                'IR sensor 2': unpacked[4]
            }
        return None

    async def get_version_string(self) -> str:
        """Get version as a human-readable string."""
        ver = await self.get_versions(0xA5)
        try:
            major = ver[1]
            minor = ver[2]
            patch = ver[9]
            if major < 32 or major > 126:
                major = str(major)
            else:
                major = chr(major)

            return '.'.join([major, str(minor), str(patch)])
        except IndexError:
            return None

    def get_touch_sensors_cached(self):
        '''Returns list of most recently seen touch sensor state, or None if no event has happened yet'''
        return super().get_touch_sensors_cached()[0:2]

    def get_cliff_sensors_cached(self):
        '''Returns tuple of most recently seen cliff sensor state'''
        return (self.cliff_sensor.left, self.cliff_sensor.front_left,
                self.cliff_sensor.front_right, self.cliff_sensor.right)

    async def get_cliff_sensors(self):
        '''Returns tuple of most recently seen cliff sensor state.
           If there were a protocol getter, this would await that response when the cache is empty.
        '''
        return self.get_cliff_sensors_cached()

    async def navigate_to_waypoint(self, waypoint: Waypoint) -> bool:
        """
        Navigate to a specific waypoint with optional heading.
        Returns True if navigation was successful, False otherwise.
        """
        self._navigation_state.current_waypoint = waypoint
        self._navigation_state.is_navigating = True

        try:
            # Check for obstacles before starting navigation
            if await self._check_for_obstacles():
                return False

            # Navigate to the waypoint
            await self.navigate_to(waypoint.x, waypoint.y, waypoint.heading)
            
            # Verify we reached the waypoint within tolerance
            if not await self._verify_waypoint_reached(waypoint):
                return False

            return True
        finally:
            self._navigation_state.is_navigating = False
            self._navigation_state.current_waypoint = None

    async def follow_waypoints(self, waypoints: List[Waypoint]) -> bool:
        """
        Follow a sequence of waypoints.
        Returns True if all waypoints were reached successfully.
        """
        self._navigation_state.waypoints = waypoints.copy()
        
        for waypoint in waypoints:
            if not await self.navigate_to_waypoint(waypoint):
                return False
                
        return True

    async def _check_for_obstacles(self) -> bool:
        """
        Check for obstacles using IR proximity sensors.
        Returns True if obstacles are detected, False otherwise.
        """
        ir_proximity = await self.get_ir_proximity()
        if ir_proximity is None:
            return False

        # Check if any sensor detects an obstacle within threshold
        for sensor_value in ir_proximity.sensors:
            if sensor_value > self.OBSTACLE_DETECTION_THRESHOLD:
                self._navigation_state.obstacle_detected = True
                self._navigation_state.last_obstacle_position = (self.pose.x, self.pose.y)
                return True

        self._navigation_state.obstacle_detected = False
        return False

    async def _verify_waypoint_reached(self, waypoint: Waypoint) -> bool:
        """
        Verify that the robot has reached the waypoint within tolerance.
        """
        if not self.USE_ROBOT_POSE:
            return True

        dx = self.pose.x - waypoint.x
        dy = self.pose.y - waypoint.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > waypoint.tolerance:
            return False

        if waypoint.heading is not None:
            heading_diff = abs(self.pose.heading - waypoint.heading)
            if heading_diff > waypoint.heading_tolerance:
                return False

        return True

    async def avoid_obstacle(self) -> bool:
        """
        Perform obstacle avoidance maneuver.
        Returns True if avoidance was successful, False otherwise.
        """
        if not self._navigation_state.obstacle_detected:
            return True

        # Get current position and heading
        current_x, current_y = self.pose.x, self.pose.y
        current_heading = self.pose.heading

        # Calculate avoidance point
        avoidance_distance = self.OBSTACLE_AVOIDANCE_DISTANCE
        avoidance_angle = 45  # degrees

        # Calculate new position for avoidance
        new_heading = current_heading + avoidance_angle
        new_x = current_x + avoidance_distance * math.cos(math.radians(new_heading))
        new_y = current_y + avoidance_distance * math.sin(math.radians(new_heading))

        # Create avoidance waypoint
        avoidance_waypoint = Waypoint(
            x=new_x,
            y=new_y,
            heading=new_heading,
            tolerance=10.0  # Larger tolerance for avoidance
        )

        # Navigate to avoidance point
        return await self.navigate_to_waypoint(avoidance_waypoint)

    async def navigate_with_obstacle_avoidance(self, x: float, y: float, heading: Optional[float] = None) -> bool:
        """
        Navigate to a point with obstacle avoidance.
        Returns True if navigation was successful, False otherwise.
        """
        waypoint = Waypoint(x=x, y=y, heading=heading)
        
        while True:
            # Check for obstacles
            if await self._check_for_obstacles():
                # Try to avoid obstacle
                if not await self.avoid_obstacle():
                    return False
                continue

            # Navigate to waypoint
            if await self.navigate_to_waypoint(waypoint):
                return True

            # If we failed to reach the waypoint, try obstacle avoidance
            if not await self.avoid_obstacle():
                return False

    def get_navigation_state(self) -> NavigationState:
        """
        Get the current navigation state.
        """
        return self._navigation_state

    async def stop_navigation(self):
        """
        Stop the current navigation task.
        """
        self._navigation_state.is_navigating = False
        self._navigation_state.current_waypoint = None
        self._navigation_state.waypoints = []
        await self.stop()
