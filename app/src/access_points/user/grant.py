from ...models import User, AccessPoint
from flask import abort


def grant(email, path, timeref):
    if not email or not path:
        abort(400, 'You have to give the user\'s email as well as the the access point\'s path.')
    try:
        user = User.query.filter_by(email=email).first()
        ap = AccessPoint.query.filter_by(path=path).first()
        if ap is None:
            raise Exception('This access point does not exist.')
        if user.grant_access_to(ap, timeref):
            return "The access to '{}' for '{}' is successfully updated.".format(path, email), 200
        return "The access to '{}' is successfully granted for '{}'.".format(path, email), 201
    except Exception as e:
        abort(500, e)
