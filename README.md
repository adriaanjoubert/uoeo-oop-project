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

# References

Stewart, J. and Kokoska, S. (2023) Calculus: Concepts and Contexts. 5th edn. Boston: Cengage.
