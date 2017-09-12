from flask import abort

from ...models import User


def add(email, password):
    if not email or not password:
        abort(400, 'You have to give the user\'s email as well as a password.')
    try:
        user = User.query.filter_by(email=email).first()
        if user is not None:
            raise Exception('This email is already taken.')
        if len(password) < 6:
            raise Exception('The password is too short.')

        user = User(email=email)

        user.hash_password(password)
        user.add()
        return "User with email '{}' is successfully created.".format(email), 201
    except Exception as e:
        abort(500, e)
