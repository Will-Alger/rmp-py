# rmp-py

## Setup Instructions

This project requires Python 3 and pip. The instructions below should work on both Windows and MacOS systems.

### Install Python and pip

If you haven't installed Python or pip yet, follow these guides:

- [Python Installation](https://www.python.org/downloads/)
- [pip Installation](https://pip.pypa.io/en/stable/installing/)

Ensure that Python and pip are in your system's PATH.

### Set up a Virtual Environment

1. Open a terminal
2. Navigate to the project directory: `cd path_to_project_directory`
3. Create a new virtual environment:
   - On MacOS: `python3 -m venv env`
   - On Windows: `py -m venv env`

### Activate the Virtual Environment

Before installing any dependencies, you should activate your virtual environment:

- On MacOS: `source env/bin/activate`
- On Windows: `.\env\Scripts\activate`

### Install Dependencies

Now that the virtual environment is activated, you can install the necessary dependencies with pip:

`pip install -r requirements.txt`

### Run the Application

After setting up the environment and installing dependencies, you can execute the test project by running main.py

---

Remember: Always ensure your virtual environment is active when running or adding dependencies to the project! To deactivate your virtual environment, just type `deactivate` in your terminal.
