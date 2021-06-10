# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

## Configuration Requirements 

The following must be done before running the Flask App. 

Create a text file, `.env`, that must have the following:
```
USER_NAME=<Mongo User Id>
PASSWORD=<Mongo password>
MONGO_URL=<Mongo DB Url>
DEFAULT_DATABASE=<Mongo DB Name>
``` 
The file must reside in the ```todo_app``` folder.

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

For e2e testing, you will need to download webdriver for Selenium - for [Chrome Webdriver](https://chromedriver.storage.googleapis.com/index.html).  I would suggest in putting the webdriver in a folder and add it to your PATH environment.

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
 * Debugger PIN: 999-999-999
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running the App on a VM (Vagrant)

This project comes with a Vagrant file that allows the ToDo app to run a VM.  You will need to download and install the following two software: Virtual Box, https://www.virtualbox.org/ and Vagrant, https://www.vagrantup.com/.  Open up a terminal console, and navigate to this project folder, type:
```bash 
vagrant up
```
If this is not done before, it will take several minutes to download an Ubuntu image from hashicorp site and do various configuration.

At the end, the output should be similar in above section on Running The App.

To end the Vagrant session, CTRL-C and kill the ruby process.

## Running the App on Docker
This project also comes with a file `dockerFile` that have two profiles: `developments` and `production`

### Creating and running a container for development
In a console, run this command:

```powershell
docker build --target developments --tag todo-app:dev .
```
To run the app server from the container:
```powershell
docker run -p 5000:5000 --env-file .\.env --mount type=bind,source="$(pwd)"/todo_app,target=/project/todo_app todo-app:dev
```
If you want to run the container in background:
```powershell
docker run -d -p 5000:5000 --env-file .\.env --mount type=bind,source="$(pwd)"/todo_app,target=/project/todo_app todo-app:dev 
```

### Creating and running a container for production
In a console, run this command:

```powershell
docker build --target production --tag todo-app:prod .
```

To run the app server from the container:
```powershell
docker run -p 5000:5000 --env-file .\.env todo-app:prod
```
If you want to run the container in background:
```powershell
docker run -d -p 5000:5000 --env-file .\.env todo-app:prod 
```

## Creating and running a container for test
In a console, run this command:

```powershell
docker build --target test --tag todo-app:test .
```

```powershell
docker run --env-file .\.env --mount type=bind,source="$(pwd)"/todo_app,target=/project/todo_app todo-app:test
```
You might expect to find the output:
```
============================= test session starts ==============================
platform linux -- Python 3.8.x, pytest-6.2.x, py-1.10.x, pluggy-0.13.x
rootdir: /project
plugins: dotenv-0.5.2
collected 12 items

tests/test_app_view_model.py .                                           [  8%]
tests/test_view_model.py .......                                         [ 66%]
tests_e2e/test_journey.py  * Serving Flask app "todo_app.app" (lazy loading)
 * Environment: development
....                                           [100%]
```

## Continuous Integration (CI) and Continuous Delivery (CD)
For CI, this project comes a configuration YAML file for Travis CI.  You will need to have an account with Travis (please visit by clicking here [Travis CI](https://travis-ci.com/signup)).  Please refer to their documentation for use.  You will need to associate your GitHub account to access this project.

The YAML file will need to be amended for the following:
* SECRET_KEY
* DOCKER_PASSWORD
* USER_NAME
* PASSWORD
* MONGO_URL
* DEFAULT_DATABASE
 
You can see they are from your .env file. Please remove any entry in the YAML file beginning with `-secure ...` in the `env` -> `global` section.  You must encrypt your values with Travis CLI (see [Encryption Keys - Usage](https://docs.travis-ci.com/user/encryption-keys#usage)).  **Note** on Docker's password - please use your generated API token, not the actual password!

For CD, the Travis YML configuration file uses Heroku Application platform - see [Heroku Sign up](https://id.heroku.com/signup/)

You will need to install/use Heroku CLI to do some configuration for values from your `.env` file such as:

``heroku config:set `cat .env | grep MONGO_URL` ``

