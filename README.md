https://github.com/adriaanjoubert/uoeo-oop-project

# Instructions
## Project setup
The application has been tested with Python 3.13.1. To create a virtual environment with this specific version of Python,
please refer to https://github.com/pyenv/pyenv.

Inside of your virtual environment, install the project dependencies with the following command:

```bash
pip install -r requirements.txt
```

## Running the application
To run the application, execute the following command in the terminal:

```bash
python main.py
```

You will be presented with a menu where you can add commands to the stack or queue and execute all the commands.

In a real-world scenario, the user will be able to add commands to the stack and queue while other commands are busy executing.

In this simulated scenario, the commands are executed instantaneously and the user can only add commands to the stack and queue before and after all the commands have been executed.

## Unit tests
To run the unit tests using `pytest`, run the following command in the terminal:

```bash
pytest tests.py --log-cli-level INFO
```

## Commentary

The robot is "turned on" by starting the application and "shut down" by choosing the exit option in the main menu.

The application illustrates dependency by having the Robot class depend on other helper classes, such as Leg and Speaker, with their own, unique methods.

The Robot class keeps track of its internal state through the attributes `facing_direction` and `position` as well as the stack and queue where it stores commands to be executed.

The application illustrates a stack and a queue. The user can add commands to the stack and queue and execute all the commands. Commands on the stack are executed first and then commands in the queue are executed.

The application is a simulation of a real world scenario. In the simulation, the commands are executed instantly by logging the action performed to stdout whereas in the real world, the commands would need to be sent to physical components and would take time to execute.

The project includes unit tests which uses mocks and asserts to confirm the expected function calls when running the application. There is also an integration test which does not mock function calls and which tests the application as a whole.

The project conforms to the PEP8 style guideline (Alchin, 2010). This can be confirmed by executing the command `flake8` inside the virtual environment and observing that no errors are returned.

# References

Alchin, M. (2010) 'PEP 8 Style Guide for Python', in: Alchin, M. Pro Python. United States: Apress L. P.

Stewart, J. and Kokoska, S. (2023) Calculus: Concepts and Contexts. 5th edn. Boston: Cengage.
