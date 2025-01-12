import logging
from math import cos, sin

from numpy import arctan2

from constants import EPSILON_DISTANCE, ROBOT_STEP_SIZE
from utils import distance_between


class Leg:

    def __init__(self, robot) -> None:
        self.robot = robot

    def step(self, destination: tuple[float, float]) -> None:
        distance_from_destination = distance_between(self.robot.position, destination)
        if distance_from_destination < ROBOT_STEP_SIZE:
            distance_to_move = distance_from_destination
        else:
            distance_to_move = ROBOT_STEP_SIZE

        self.robot.position = (
            self.robot.position[0] + distance_to_move * cos(self.robot.facing_direction),
            self.robot.position[1] + distance_to_move * sin(self.robot.facing_direction),
        )


class Robot:
    facing_direction: float
    position: tuple[float, float]

    def __init__(self) -> None:
        self.facing_direction = 0.0
        self.position = (0.0, 0.0)
        self.left_leg = Leg(robot=self)
        self.right_leg = Leg(robot=self)

    def move(self, destination: tuple[float, float]) -> None:
        logging.info(f"Moving to {destination}")

        while True:
            self.left_leg.step(destination=destination)
            if distance_between(self.position, destination) < EPSILON_DISTANCE:
                break
            self.right_leg.step(destination=destination)
            if distance_between(self.position, destination) < EPSILON_DISTANCE:
                break

        logging.info(f"Arrived at {destination}")

    def turn(self, destination: tuple[float, float]) -> None:
        logging.info(f"Turning towards {destination}")
        angle = arctan2(destination[1] - self.position[1], destination[0] - self.position[0])
        self.facing_direction = angle
        logging.info(f"Now facing {angle}")
