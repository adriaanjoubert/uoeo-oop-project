import logging
from dataclasses import dataclass
from math import cos, sin, pi
from queue import Queue, LifoQueue
from typing import Any

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
        distance_from_destination = distance_between(
            self.robot.position,
            destination,
        )
        if distance_from_destination < ROBOT_STEP_SIZE:
            distance_to_move = distance_from_destination
        else:
            distance_to_move = ROBOT_STEP_SIZE

        # In a real-world scenario we would send an instruction to the limb
        # to move in a certain way to accomplish a step motion. Here we just
        # update the robot's position.
        self.robot.position = (
            self.robot.position[0]
            + distance_to_move * cos(self.robot.facing_direction),
            self.robot.position[1]
            + distance_to_move * sin(self.robot.facing_direction),
        )


class Speaker:

    def speak(self, message: str) -> None:
        # In a real-world scenario we would convert the text to a speech audio
        # file and send an instruction to the speaker play the audio file.
        logging.info(f"Message played over the speaker: {message}")
        return


@dataclass
class Command:
    kwargs: dict[str, Any]
    operation: str


class Robot:
    command_queue: Queue
    command_stack: LifoQueue
    facing_direction: float
    position: tuple[float, float]

    def __init__(self) -> None:
        self.command_queue = Queue()
        self.command_stack = LifoQueue()
        self.facing_direction = 0.0
        self.position = (0.0, 0.0)
        self.left_leg = Leg(robot=self)
        self.right_leg = Leg(robot=self)
        self.speaker = Speaker()

    def _collect_command(self) -> Command:
        print("Available commands:")
        print("1. Move")
        print("2. Lift")
        print("3. Speak")
        match input():
            case "1":
                print("Enter destination in the format x,y, e.g. 1,2")
                x, y = input().split(",")
                return Command(
                    kwargs={"destination": (float(x), float(y))},
                    operation="move",
                )
            case "2":
                print("Enter object location in the format x,y, e.g. 1,2")
                x, y = input().split(",")
                return Command(
                    kwargs={"object_location": (float(x), float(y))},
                    operation="lift",
                )
            case "3":
                print("Enter message to speak")
                message = input()
                return Command(kwargs={"message": message}, operation="speak")

    def run(self) -> None:
        while True:
            print("Main menu")
            print("1. Add command to stack")
            print("2. Add command to queue")
            print("3. Execute commands")
            print("4. Exit")
            match input():
                case "1":
                    print("Enter command to add to stack")
                    command = self._collect_command()
                    self.command_stack.put(command)
                    print("Command added to stack")
                case "2":
                    print("Enter command to add to queue")
                    command = self._collect_command()
                    self.command_queue.put(command)
                    print("Command added to queue")
                case "3":
                    pass
                case "4":
                    return

            while not self.command_stack.empty():
                command = self.command_stack.get()
                self._execute(command=command)
            while not self.command_queue.empty():
                command = self.command_queue.get()
                self._execute(command=command)

            logging.info("All commands executed")

    def _is_at(self, location: tuple[float, float]) -> bool:
        # The robot is defined to be at location if the distance between
        # self.position and location is less than EPSILON_DISTANCE
        return distance_between(self.position, location) < EPSILON_DISTANCE

    def turn(self, destination: tuple[float, float]) -> None:
        logging.info(f"Turning towards {destination}")
        angle = arctan2(
            destination[1] - self.position[1],
            destination[0] - self.position[0],
        )
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
        logging.info(f"Object at {object_location} has been lifted")

    def speak(self, message: str) -> None:
        self.speaker.speak(message=message)

    def _execute(self, command: Command) -> None:
        method = getattr(self, command.operation)
        method(**command.kwargs)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    robot = Robot()
    robot.run()
