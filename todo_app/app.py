import json
import os
from flask_login.login_manager import LoginManager
from flask_login.utils import login_required, login_user
from todo_app.data.mongo_items import Mongo_service
from todo_app.app_config import Config
from todo_app.viewmodel import ViewModel
from todo_app.data.user_role import writer_required, isWriterRole
from flask import Flask, render_template, request, redirect, url_for, g
from oauthlib.oauth2 import WebApplicationClient
import requests
from todo_app.data.TodoUser import ToDoUser
from werkzeug.debug import DebuggedApplication
import todo_app.data.mongo_constants as constants
from flask_login import current_user

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    github_id = os.getenv('GITHUB_CLIENT')
    github_secret = os.getenv('GITHUB_SECRET')

    client = WebApplicationClient(github_id)

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    with app.app_context():
        service = Mongo_service()
        service.initiate()
    
    login_manager = LoginManager()
    @login_manager.unauthorized_handler
    def unauthenticated():
        uri = 'https://github.com/login/oauth/authorize'
        redirect_url = client.prepare_request_uri(uri)
        return redirect(redirect_url)
    
    @login_manager.user_loader
    def load_user(user_id):
        return ToDoUser(id=user_id)
    
    login_manager.init_app(app)

    @app.route('/')
    @login_required
    def index():
        service.get_lists()
        todos = service.get_items()
        sort = request.values.get("sort", "")
        if sort == "asc":
            todos = sorted(todos, key=lambda k: k.status)
        elif sort == "desc":
            todos = sorted(todos, key=lambda k: k.status, reverse=True)

        item_view_model = ViewModel(todos)
        return render_template('index.html', view_model = item_view_model, writer_required = isWriterRole(current_user.id))

    @app.route('/new_todo', methods=['POST'])
    @login_required
    @writer_required
    def add_item_from_form():
        title = request.form['title']
        service.add_item(title)

        return redirect(url_for('index'))

    @app.route('/update_todo/<id>', methods=['POST'])
    @login_required
    @writer_required
    def update_item(id):
        item = service.get_item(id)
        listId = service.get_list_id(constants.TODO_APP_COMPLETED)
        
        if request.form.get('done'):
            item.status= constants.TODO_APP_COMPLETED
        else:
            listId = service.get_list_id(constants.TODO_APP_DOING)
            item.status = constants.TODO_APP_DOING
            
        item.listId = listId
        service.save_item(item)
        return redirect(url_for('index'))

    @app.route('/remove_todo/<id>', methods=['GET'])
    @login_required 
    @writer_required
    def remove_todo(id):
        service.remove_item(id)
        return redirect(url_for('index'))

    @app.route('/login/')
    def login():
        git_code = request.args['code']
        client = WebApplicationClient(github_id, code=git_code)
        client.parse_request_uri_response(request.url)
        body = {
           "client_id": github_id,
           "client_secret": github_secret,
           "code": git_code
        }
        response = requests.post('https://github.com/login/oauth/access_token', data=body)
        client.parse_request_body_response(response.text)
        user_uri, headers, body = client.add_token("https://api.github.com/user")
        user_response = requests.get(user_uri, headers=headers).text
        gitUser = json.loads(user_response)
        login_user(gitUser["id"])
        return redirect(url_for('index'))

    if __name__ == '__main__':
        app.run()

    return app