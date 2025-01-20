from unittest import TestCase
from unittest.mock import patch, MagicMock

from main import Robot, Command


class RobotTestCase(TestCase):

    @patch("main.input")
    def test_run(self, mock_input: MagicMock) -> None:
        mock_input.side_effect = ["3", "4"]
        robot = Robot()
        robot.command_queue.put(Command(kwargs={"object_location": (0.0, 0.0)}, operation="lift"))
        robot.command_queue.put(Command(kwargs={"message": "Hello, world!"}, operation="speak"))
        robot.command_stack.put(Command(kwargs={"destination": (1.0, 0.0)}, operation="move"))
        robot.command_stack.put(Command(kwargs={"destination": (1.0, 1.0)}, operation="move"))
        robot.command_stack.put(Command(kwargs={"destination": (0.0, 1.0)}, operation="move"))
        robot.run()
