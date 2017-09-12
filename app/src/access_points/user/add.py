from ...models import User
from flask import abort



def add(email, password, adminBool, access_points):
    if not email or not password:
        abort(400, 'You have to precise the user\'s email as well as a password.')
    try:
        if adminBool:
            user = User(email=email, admin=True)
        else:
            user = User(email=email, admin=False)
            
        user.hash_password(password)
        user.save_user()
        if type(access_points) is list:
            for ap in access_points:
                path = ap['path']
                timeref = ap['timeref']
                user.grant_access_to(path, timeref)
        return "User with email '{}' is successfully created.".format(email), 201
    except Exception as e:
        abort(500, e)
