# octorun

modular centralized controller for github self-hosted runners


## Overview

This project is a Python application designed to demonstrate the use of Docker and Docker Compose for containerization. It includes a simple structure with a main application file, unit tests, and configuration files for packaging and dependencies.

## Project Structure

```sh
octorun
├── src
│   └── my_python_project
│       ├── __init__.py
│       └── main.py
├── tests
│   └── test_main.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── setup.py
├── requirements.txt
└── README.md
```

## Installation

To install the project, you can use pip. First, ensure you have Python and pip installed on your machine. Then, run the following command:

```sh
pip install .
```

This will install the package along with its dependencies as specified in `pyproject.toml` and `requirements.txt`.

## Running the Application

To run the application, you can use Docker Compose. First, build the Docker image:

```sh
docker-compose build
```

Then, start the application:

```sh
docker-compose up
```

## Running Tests

To run the unit tests, you can use pytest or unittest. If you have pytest installed, run:

```sh
pytest tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
