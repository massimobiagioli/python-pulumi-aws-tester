# Test Project with Pulumi and FastAPI on AWS

This project is an example of using Pulumi to create infrastructure on AWS and utilizing FastAPI to develop a web application.

## Description

The project aims to demonstrate how to use Pulumi, an infrastructure as code provisioning and management tool, to create and manage resources on AWS. 

Additionally, the project utilizes FastAPI, a modern web framework for building APIs in Python. FastAPI offers high execution speed and easy handling of HTTP requests.

## Project Structure

The project is organized as follows:

- `main.py`: the main file that contains the code for creating the infrastructure using Pulumi.
- `app.py`: the file that contains the code for the FastAPI application.
- `requirements.txt`: the file that lists the project dependencies.
- `README.md`: the file that describes the project.

## Prerequisites

Before running the project, make sure you have the following components installed:

- Python 3.12
- Pulumi
- FastAPI

## Execution Instructions

To run the project, follow these steps:

1. Clone the repository to your computer.
2. Install the dependencies with `make install-dev`
3. Configure your AWS access credentials in your environment.
4. Run the `pulumi up` command to create the infrastructure on AWS.
5. Run the `make start-local` command to start the FastAPI application.
