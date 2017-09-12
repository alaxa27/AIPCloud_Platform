from flask import abort

from ...models import User


def delete(email):
    if not email:
        abort(400, 'You have to give the user\'s email.')
    try:
        user = User.query.filter_by(email=email).first()
        if user is None:
            raise Exception('This user does not exist.')

        user.delete()
        return "User with email '{}' is successfully deleted.".format(email), 201
    except Exception as e:
        abort(500, e)
