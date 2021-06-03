from flask_login import UserMixin

class ToDoUser(UserMixin):
    def __init__(self, id):
        self.id = id

