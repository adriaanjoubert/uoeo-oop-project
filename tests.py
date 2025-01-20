from unittest import TestCase
from unittest.mock import patch, MagicMock, call

from main import Robot, Command


class RobotTestCase(TestCase):

    @patch("main.input")
    def test_collect_command(self, mock_input: MagicMock) -> None:
        robot = Robot()
        mock_input.side_effect = ["1", "1,2"]
        command = robot._collect_command()
        self.assertEqual(command.operation, "move")
        self.assertEqual(command.kwargs["destination"], (1.0, 2.0))

    @patch("main.Robot._execute")
    @patch("main.Robot._collect_command")
    @patch("main.input")
    def test_run(
        self,
        mock_input: MagicMock,
        mock_collect_command: MagicMock,
        mock_execute: MagicMock,
    ) -> None:
        mock_input.side_effect = ["2", "2", "1", "1", "1", "3", "4"]
        command_1 = Command(
            kwargs={"object_location": (0.0, 0.0)},
            operation="lift",
        )
        command_2 = Command(
            kwargs={"message": "Hello, world!"},
            operation="speak",
        )
        command_3 = Command(
            kwargs={"destination": (1.0, 0.0)},
            operation="move",
        )
        command_4 = Command(
            kwargs={"destination": (1.0, 1.0)},
            operation="move",
        )
        command_5 = Command(
            kwargs={"destination": (0.0, 1.0)},
            operation="move",
        )
        mock_collect_command.side_effect = [
            command_1,
            command_2,
            command_3,
            command_4,
            command_5,
        ]
        robot = Robot()
        robot.run()
        mock_execute.assert_has_calls(
            [
                call(command=command_1),
                call(command=command_2),
                call(command=command_3),
                call(command=command_4),
                call(command=command_5),
            ]
        )


class RobotIntegrationTestCase(TestCase):

    @patch("main.input")
    def test_run(self, mock_input: MagicMock) -> None:
        mock_input.side_effect = ["3", "4"]
        robot = Robot()
        robot.command_queue.put(
            Command(
                kwargs={"object_location": (0.0, 0.0)},
                operation="lift",
            )
        )
        robot.command_queue.put(
            Command(
                kwargs={"message": "Hello, world!"},
                operation="speak",
            )
        )
        robot.command_stack.put(
            Command(
                kwargs={"destination": (1.0, 0.0)},
                operation="move",
            )
        )
        robot.command_stack.put(
            Command(
                kwargs={"destination": (1.0, 1.0)},
                operation="move",
            )
        )
        robot.command_stack.put(
            Command(
                kwargs={"destination": (0.0, 1.0)},
                operation="move",
            )
        )
        robot.run()
