import io
import json
import os

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