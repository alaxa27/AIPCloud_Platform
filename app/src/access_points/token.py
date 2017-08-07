from flask import abort, jsonify
from time import time

def generate_token(user):
    if user.admin:
        token = user.generate_auth_token(604800)
        return jsonify({'token': token.decode('ascii'), 'expires-in': "1 week" })
    else:
        auths = user.points
        counter = 0
        l = []
        for element in auths:
            if element.timeref >= int(time()):
                l.append(element.timeref)
                counter = 1
        if counter == 0:
            abort(403)
        timeref = max(l)
        expiration = timeref - int(time())
        if expiration <= 0:
            abort(403)
        m, s = divmod(expiration, 60)
        h, m = divmod(m, 60)
        token = user.generate_auth_token(expiration)
        return jsonify({'token': token.decode('ascii'), 'expires_in': "%dh %02dmin %02ds" % (h, m, s)})
