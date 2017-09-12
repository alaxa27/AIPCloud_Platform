from ...models import User, AccessPoint
from flask import abort


def adminify(email):
    if not email:
        abort(400, 'You have to give the user\'s email.')
    try:
        user = User.query.filter_by(email=email).first()
        if user is None:
            raise Exception('User with email: {} does not exist.'.format(email))
        user.adminify()
        return 'User {} is now an admin.'.format(email), 201
    except Exception as e:
        abort(500, e)
