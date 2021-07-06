# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

## Configuration Requirements 

The following must be done before running the Flask App. 

Create a text file, `.env`, that must have the following:
```
FLASK_APP=<default: todo_app/app>
FLASK_ENV=<default: development>
USER_NAME=<Mongo User Id>
PASSWORD=<Mongo password>
MONGO_URL=<Mongo DB Url>
DEFAULT_DATABASE=<Mongo DB Name>
MONGO_PREFIX=<Prefix>
MONGO_CONFIG=<Configuration string>
GITHUB_CLIENT_ID=<client id>
GITHUB_SECRET=<GitHub secret>
USERS_ROLE=<json file>
OAUTHLIB_INSECURE_TRANSPORT=<use the value of 1 for development>
LOGIN_DISABLED=<use False for development>
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

## Authentication
We are using GitHub OAuth2 for authentication so you will need to have an account there. Please follow the Github [documentation](https://docs.github.com/en/developers/apps/building-oauth-apps/creating-an-oauth-app) to create your oauth app.

For the callback add a particular path to this URL for example /login/ callback.

You will need both a client-id and client-secret for your .env file (respectively `GITHUB_CLIENT_ID=<client id>`, `GITHUB_SECRET=<GitHub secret>`).

NOTE: The client-secret once generated will only be shown once, so take a note of it to avoid needing to regenerate one later.  If you are doing development and do not want to use Authentication, then set LOGIN_DISABLED to False and OAUTH_INSECURE_TRANSPORT to 1 in your `.env` file

### Authorised users
To give a user permission to manage ToApps, you will need to obtain their id by using this REST API (https://api.github.com/users/<user name>`)
```json
[
    {"id": "<github id>", "role": "writer"}
]
```

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

For end-to-end testing:
```powershell
docker build --target test_e2e --tag todo-app:test_e2e .
```

```powershell
docker run --env-file .\.env --mount type=bind,source="$(pwd)"/todo_app,target=/project/todo_app todo-app:test_e2e
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

## Continuous Integration (CI)
For CI, this project comes a configuration YAML file for Travis CI.  You will need to have an account with Travis (please visit by clicking here [Travis CI](https://travis-ci.com/signup)).  Please refer to their documentation for use.  You will need to associate your GitHub account to access this project.

In Travis' setting, you must add the following:
* USER_NAME
* PASSWORD
* MONGO_URL
* DEFAULT_DATABASE
* MONGO_CONFIG

Travis will obfuscate the value for each variable; and you will not be able to see them (even in its logs) once you've added them!  

The YAML file will need to be amended for the following:
* SECRET_KEY
* DOCKER_PASSWORD
 
You can see they are from your .env file. Please remove any entry in the YAML file beginning with `-secure ...` in the `env` -> `global` section.  You must encrypt your values with Travis CLI (see [Encryption Keys - Usage](https://docs.travis-ci.com/user/encryption-keys#usage)).  **Note** on Docker's password - please use your generated API token, not the actual password!

## Continuous Delivery (CD)

For Azure, it is assumed that you have a account setup.  We are using CosmosDB and App Service. You can use its Portal or CLI to setup the above services. The following is the required step. 

### Set up a resource group 
You can navigate, in Portal, to Resource Groups and click the create link.

```dotnetcli
az group create -l uksouth -n <resource_group_name> 
```

### Set up a CosmosDB
In Portal, go to CosmsoDB and click new.  Select the option `Azure Cosmos DB for MongoDB API`

```dotnetcli
az cosmosdb create --name <cosmos_account_name> --resourcegroup <resource_group_name> --kind MongoDB

az cosmosdb mongodb database create --account-name <cosmos_account_name> --name <database_name> --resourcegroup
<resource_group_name>
```

When this is setup, go to the Connection String page in Portal or

```dotnetcli
az cosmosdb keys list -n <cosmos_account_name> -g <resource_group_name> --type connection-strings
```

### Setup an App Services

In portal, create a App Service and please ensure that you use Docker Container in the 'Publish' field.  As well as entering your image name in 'Image Source' field.

```dotnetcli
az appservice plan create --resource-group <resource_group_name> -n <appservice_plan_name> --sku Free --is-linux

az webapp create --resource-group <resource_group_name> --plan <appservice_plan_name> --name <webapp_name> --deployment-container-image-name <dockerhub_username>/todoapp:latest
```

Set up the environment variables in the App Services' Settings -> Configuration

```dotnetcli
az webapp config appsettings set -g <resource_group_name> -n <webapp_name> --settings FLASK_APP=todo_app/app.
```

Browse to `http://<webapp_name>.azurewebsites.net/` to check that your application works!

In App Services' Deployment Centre - enable the flag 'Enable CD'
```dotnetcli
az webapp deployment container config --enable-cd true --resource-group <resource_group_name> --name <webapp_name>
```

The page contains a field for Webhook - click on the 'eye' icon to reveal the URL.  You can test this in Postman or use CURL:
```dotnetcli
curl -dH -X POST "https://\$<deployment_username>:<deployment_password>@<webapp_name>.scm.azurewebsites.net/docker/hook"
```
Use this URL in your Travis's deploy section:

```yml
    deploy:
      provider: script
      script:
      - curl -dH -X POST '$AZURE_WEBHOOK'
      on:
        all_branches: true
```
