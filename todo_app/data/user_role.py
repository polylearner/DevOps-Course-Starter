import io
import json
import os
from functools import wraps
from flask_login import current_user
from flask import request, redirect, url_for

def isReaderRole(userId):
    for user in getUsersRole():
        if user['id'] == userId:
            if user['role'] == 'reader':
                return True

    return False

def isWriterRole(userId):
    for user in getUsersRole():
        if user['id'] == userId:
            if user['role'] == 'writer':
                return True

    return False

def getUsersRole():
    usersRoleFilePath = os.getenv('USERS_ROLE')
    with io.open(usersRoleFilePath) as f:
        usersRole = json.loads(f.read())
    return usersRole

def writer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not isWriterRole(current_user.id):
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function