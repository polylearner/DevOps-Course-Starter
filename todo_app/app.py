from flask_login.login_manager import LoginManager
from flask_login.utils import login_required
from todo_app.data.mongo_items import Mongo_service
from todo_app.app_config import Config
from todo_app.viewmodel import ViewModel
from flask import Flask, render_template, request, redirect, url_for
import oauthlib

from todo_app.data.item import Item
from werkzeug.debug import DebuggedApplication
import todo_app.data.mongo_constants as constants

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    with app.app_context():
        service = Mongo_service()
        service.initiate()
    
    login_manager = LoginManager()
    @login_manager.unauthorized_handler
    def unauthenticated():
        pass # Add logic to redirect to the
             # Github OAuth flow when unauthenticated
    
    @login_manager.user_loader
    def load_user(user_id):
        return None
    
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
        return render_template('index.html', view_model = item_view_model)

    @app.route('/new_todo', methods=['POST'])
    @login_required
    def add_item_from_form():
        title = request.form['title']
        service.add_item(title)
        return redirect(url_for('index'))

    @app.route('/update_todo/<id>', methods=['POST'])
    @login_required
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
    def remove_todo(id):
        service.remove_item(id)
        return redirect(url_for('index'))

    if __name__ == '__main__':
        app.run()

    return app