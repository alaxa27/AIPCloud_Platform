from flask import abort

from ...models import User, AccessPoint
from .grant import grant


def add(email, password, adminBool):
    if not email or not password:
        abort(400, 'You have to give the user\'s email as well as a password.')
    try:
        if adminBool:
            user = User(email=email, admin=True)
        else:
            user = User(email=email, admin=False)

        user.hash_password(password)
        user.save_user()
        return "User with email '{}' is successfully created.".format(email), 201
    except Exception as e:
        abort(500, e)
