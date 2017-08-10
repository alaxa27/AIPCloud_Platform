from ..models import User, AccessPoint, Authorization
from .. import db
from flask import abort, jsonify
from time import time


def grant(email, route):
    try:
        if not email or not route:
            abort(400, 'You have to precise the user\'s email as well as the route of the access point.')
        user = User.query.filter_by(email=email).first()
        ap = AccessPoint.query.filter_by(path=route).first()
        auth = Authorization(timeref = int(time()) + 86400)
        auth.point = ap
        user.grant_access_to(auth)
        db.session.commit()
        return 'The access to the point is successfully granted.', 201
    except Exception as e:
        abort(500, e)
