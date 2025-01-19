import logging
from math import cos, sin, pi

from numpy import arctan2

from constants import EPSILON_DISTANCE, ROBOT_STEP_SIZE
from utils import distance_between


class Joint:
    angle: float

    def __init__(self) -> None:
        # For the sake of simplicity we initialize the joint with an angle of
        # 180 degrees (pi), i.e., the limb is straight. In a real-world
        # scenario we would store the angle at shutdown and re-calibrate it on
        # boot, and we may want to redesign this model of the joint to bend by
        # coordinated motion of the limb parts connected by the joint.
        self.angle = pi

    def rotate(self, angle: float) -> None:
        self.angle = angle


class Leg:
    knee: Joint

    def __init__(self, robot) -> None:
        self.knee = Joint()
        self.robot = robot

    def step(self, destination: tuple[float, float]) -> None:
        distance_from_destination = distance_between(self.robot.position, destination)
        if distance_from_destination < ROBOT_STEP_SIZE:
            distance_to_move = distance_from_destination
        else:
            distance_to_move = ROBOT_STEP_SIZE

        # In a real-world scenario we would send an instruction to the limb
        # to move in a certain way to accomplish a step motion. Here we just
        # update the robot's position.
        self.robot.position = (
            self.robot.position[0] + distance_to_move * cos(self.robot.facing_direction),
            self.robot.position[1] + distance_to_move * sin(self.robot.facing_direction),
        )


class Speaker:

    def speak(self, message: str) -> None:
        # In a real-world scenario we would convert the text to a speech audio
        # file and send an instruction to the speaker play the audio file.
        logging.info(f"Message played over the speaker: {message}")
        return

class Robot:
    facing_direction: float
    position: tuple[float, float]

    def __init__(self) -> None:
        self.facing_direction = 0.0
        self.position = (0.0, 0.0)
        self.left_leg = Leg(robot=self)
        self.right_leg = Leg(robot=self)
        self.speaker = Speaker()

    def _is_at(self, location: tuple[float, float]) -> bool:
        # The robot is defined to be at location if the distance between
        # self.position and location is less than EPSILON_DISTANCE
        return distance_between(self.position, location) < EPSILON_DISTANCE

    def turn(self, destination: tuple[float, float]) -> None:
        logging.info(f"Turning towards {destination}")
        angle = arctan2(destination[1] - self.position[1], destination[0] - self.position[0])
        self.facing_direction = angle
        logging.info(f"Now facing {angle}")

    def move(self, destination: tuple[float, float]) -> None:
        logging.info(f"Moving to {destination}")

        self.turn(destination=destination)

        while not self._is_at(location=destination):
            self.left_leg.step(destination=destination)
            if self._is_at(location=destination):
                break
            self.right_leg.step(destination=destination)

        logging.info(f"Arrived at {destination}")

    def _bend_knees(self, angle: float) -> None:
        # TODO: bend both knees simultaneously to avoid losing balance.
        self.left_leg.knee.rotate(angle=angle)
        self.right_leg.knee.rotate(angle=angle)

    def _extend_arms(self) -> None:
        # In a real-world situation we would send instructions to the arms to
        # extend them.
        return

    def _position_hands_for_grasp(self) -> None:
        # In a real-world situation we would send instructions to the hands to
        # position them for grasping an object.
        return

    def _grasp(self) -> None:
        # In a real-world situation we would send instructions to the hands to
        # grasp an object.
        return

    def lift(self, object_location: tuple[float, float]) -> None:
        self.move(destination=object_location)
        self._bend_knees(angle=pi/2)  # Rotate knee joints to 90 degrees (pi/2)
        self._extend_arms()
        self._position_hands_for_grasp()
        self._grasp()
        self._bend_knees(angle=pi)  # Straighten legs

    def speak(self, message: str) -> None:
        self.speaker.speak(message=message)
