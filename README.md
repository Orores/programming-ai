# programming-ai
AI assistant for programming

## Setting up a Virtual Environment

### Setting Up a Virtual Environment (venv) for Python

#### Step 1: Prerequisites

Before you begin, make sure you have Python and pip installed on your system. You can check their versions using the following commands:

```bash
python --version
pip --version
```

#### Step 2: Create a Project Directory

Create a directory for your Python project if you haven't already. You can do this with the `mkdir` command:

```bash
mkdir my_python_project
cd my_python_project
```

#### Step 3: Initialize the Virtual Environment

To create a virtual environment, you can use the `venv` module that comes with Python. Run the following command to create a new virtual environment named "venv" in your project directory:

```bash
python -m venv venv
```

This command will create a folder named "venv" containing the virtual environment.

#### Step 4: Activate the Virtual Environment

Before you can start using the virtual environment, you need to activate it. On macOS and Linux, use the following command:

```bash
source venv/bin/activate
```

On Windows, use the following command:

```bash
venv\Scripts\activate
```

You will see the virtual environment's name appear in your terminal prompt, indicating that it's active.

#### Step 5: Install Python Packages

Now that you're in the virtual environment, you can use `pip` to install Python packages without affecting your system-wide Python installation. For example:

```bash
pip install package_name
```

#### Step 6: Deactivate the Virtual Environment

When you're done working in the virtual environment, you can deactivate it using the following command:

```bash
deactivate
```

This will return you to the global Python environment.

## Running Tests

To run tests for this project, follow these steps:

1. Make sure you have set up and activated your virtual environment as described above.

2. Navigate to the project's root directory.

3. Run the tests using the following command, which captures both standard output and standard error and saves them to a log file named `output.log`:

```bash
python -u -m unittest discover -s tests > output.log 2>&1
```

This command will discover and run all test cases in the `tests` directory while capturing any output or errors.

4. View the test results in the `output.log` file to ensure that everything is working correctly.

Now you know how to set up a virtual environment for your project, run tests, and capture the output for future reference.
