# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

## Configuration Requirements 

The following must be done before running the Flask App. 

Amend the .env that must have the following:
```
TRELLO_KEY=<Trello API key>
TRELLO_TOKEN=<Trello API token>
TRELLO_BOARD_ID = '<id>'
USE_VCR = 'False'
``` 
The file must exists in the project folder level.

Note on `USE_VCR` - this is a string flag ('True' or 'False') allowing VCR py to record HTTP requests and responses from Trello API.  Set this to 'True' only when you need to capture them.  VCR will write several 'cassette' in the tests\vcr_cassettes folder.  You will need to do this before running the PyTest class, `test_trello_data_with_vcr.py`.

At your Trello workspace, create three boards, 'To Do', 'Doing'  and 'Done'.  You will need to use Postman to obtain the board's id.  This id needs to be placed in an constant, ```TRELLO_BOARD_ID``` from the constants file ```todo_app\data\trello_constants.py```

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.tempalate` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.
