# Build a Docker Image and Container

Welcome to the `Image Builder` repository, where we aim to demystify basic arbitrage strategies and empower aspiring blockchain developers to experience the world of arbitrage. We provide comprehensive code documentation and step-by-step instructions to make learning accessible, allowing developers to grasp the concepts and eventually craft their own effective strategies.

## Table of Contents
1. [Overview](#overview)
2. [Quick Start](#quick-start) `./image_builder.py --config-file './config_file' --build-image`
3. [Setup](#setup)
    - [Building the Docker Image](#building-the-docker-image)
    - [Configuration](#configuration)
4. [Usage](#usage)
5. [File Structure](#file-structure)
6. [Unit Testing](#unit-testing)
    - [Running Unit Tests](#running-unit-tests)
    - [Test Files](#test-files)
7. [Contributing](#contributing)
8. [License](#license)

## Overview
Provide a brief description of the project, its purpose, and its functionality.

## Quick Start

Arbitrage is a trading strategy that capitalizes on price differences for the same asset across different markets. It involves buying low on one market and selling high on another to turn a profit.

## Setup
Instructions on setting up the project environment. Include steps to install Docker, clone the repository, and any other prerequisites.

### Building the Docker Image
Explain how to use `Dockerfile` and `build_and_create.py` to build the Docker image.

### Configuration
Details on how to modify `config.json` for custom settings.

## Usage
Instructions on how to run the project, including commands and any necessary arguments or flags.

```bash
./image-builder.py --help
usage: image-builder.py [-h] [-c CONFIG_FILE] [-v] [-l] [-b [BUILD_IMAGE]] [-cc] [-t]

Docker Management Script

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        Path to the configuration file
  -v, --verbose         Enable output
  -l, --logging         Enable logging
  -b [BUILD_IMAGE], --build-image [BUILD_IMAGE]
                        Build Docker image, optionally specify a Dockerfile path
  -cc, --create-container
                        Create Docker container
  -t, --run-tests       Run unit tests
  ```
## File Structure
```
.
├── image-builder
├── run_unit_tests
├── config_files
│   ├── .env
│   ├── config.json
│   ├── Dockerfile
├── docker_manager
│   ├── init.py
│   ├── docker_config.py
│   ├── docker_container_manager.py
│   ├── docker_dependency_checker.py
│   ├── docker_image_builder.py
│   ├── docker_service_manager.py
│   └── docker_utility.py
└── unittest_docker_manager 
    ├── __init__.py
    ├── test_docker_config.py
    ├── test_docker_container_manager.py
    ├── test_docker_dependency_checker.py
    ├── test_docker_image_builder.py
    ├── test_docker_service_manager.py
    └── test_docker_utility.py
```
### Dockerfile
Brief description of the Dockerfile, including its role in setting up the Docker environment for the project.

### build_and_create.py
A script that automates the building and creation of Docker containers. Describe its functionality and how it interacts with other components.

### config.json
Configuration file containing necessary settings and parameters for the project. Outline the key configuration options available.

## docker_manager
A module containing various utilities and managers for Docker operations.

### Module Files

- `docker_config.py`: Docker configuration management.
- `docker_container_manager.py`: Docker container lifecycle management.
- `docker_dependency_checker.py`: checking necessary dependencies.
- `docker_image_builder.py`: Docker image building functionality.
- `docker_service_manager.py`: managing Docker services.
- `docker_utility.py`: Various utility functions used in Docker operations.

#### docker_config.py
Manages Docker configuration settings. Describe how it reads and applies configurations from `config.json`.

#### docker_container_manager.py
Handles operations related to Docker containers such as creation, starting, stopping, and removing containers.

#### docker_dependency_checker.py
Checks for dependencies required by the Docker environment and ensures they are met.

#### docker_image_builder.py
Script for building Docker images based on specifications in `Dockerfile` and `config.json`.

#### docker_service_manager.py
Manages Docker services, including starting, stopping, and managing service-related configurations.

#### docker_utility.py
Provides utility functions for common Docker operations, enhancing code reuse and modularity.

## Unit Testing

The project includes a suite of unit tests to ensure the reliability and correctness of its functionality. These tests cover various components of the Docker manager and the core logic of the bot.

### Running Unit Tests
To run the unit tests, execute the `run_unit_tests.py` script from the project root directory:

```bash
./test_runner.py
```

This script will automatically discover and run all test cases in the `unittest_docker_manager` directory, including tests for Docker configuration, container management, dependency checking, image building, service management, and utility functions.

### Test Files
Our unit tests are organized as follows:

- `test_docker_config.py`: Tests for Docker configuration management.
- `test_docker_container_manager.py`: Tests for Docker container lifecycle management.
- `test_docker_dependency_checker.py`: Tests for checking necessary dependencies.
- `test_docker_image_builder.py`: Tests for Docker image building functionality.
- `test_docker_service_manager.py`: Tests for managing Docker services.
- `test_docker_utility.py`: Tests for various utility functions used in Docker operations.

## Contributing
We welcome contributions! Please read our contributing guidelines to learn how you can contribute to the Arbitrage-Bot project.

## License
This project is licensed under the [MIT License](LICENSE). See the LICENSE file for more details.
