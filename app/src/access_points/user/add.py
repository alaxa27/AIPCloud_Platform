from flask import abort

from ...models import User, AccessPoint
from .grant import grant


def add(email, password, adminBool, access_points):
    if not email or not password:
        abort(400, 'You have to precise the user\'s email as well as a password.')
    try:
        if adminBool:
            user = User(email=email, admin=True)
        else:
            user = User(email=email, admin=False)

        user.hash_password(password)
        if type(access_points) is list:
            for ap in access_points:
                path = ap['path']
                try:
                    timeref = ap['timeref']
                except:
                    timeref = None

                accessP = AccessPoint.query.filter_by(path=path).first()
                if accessP is not None:
                    user.grant_access_to(accessP, timeref)
                else:
                    raise Exception('One of the access_points provided does not exist.')
        user.save_user()
        return "User with email '{}' is successfully created.".format(email), 201
    except Exception as e:
        abort(500, e)
