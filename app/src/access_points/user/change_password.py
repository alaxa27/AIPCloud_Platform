from flask import abort

from ...models import User


def change_password(email, password):
    if not email or not password:
        abort(400, 'You have to give the user\'s email as well as a password.')
    try:
        user = User.query.filter_by(email=email).first()
        if user is None:
            raise Exception('This user does not exist.')

        user.hash_password(password)
        user.save()
        return "User with email '{}'\'s password has succesfully changed.".format(email), 201
    except Exception as e:
        abort(500, e)
