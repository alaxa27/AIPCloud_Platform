from ...models import User, AccessPoint
from flask import abort


def grant(email, route, timeref):
    if not email or not route:
        abort(400, 'You have to precise the user\'s email as well as the route of the access point.')
    try:
        user = User.query.filter_by(email=email).first()
        ap = AccessPoint.query.filter_by(path=route).first()
        if user.grant_access_to(ap, timeref):
            return "The access to '{}' for '{}' is successfully updated.".format(route, email), 200
        return "The access to '{}' is successfully granted for '{}'.".format(route, email), 201
    except Exception as e:
        abort(500, e)
