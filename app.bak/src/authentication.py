from .models import User
from flask import g
from time import time


class Authentication(object):

    def verify_password(self, email_or_token, password):
        # first try to authenticate by token
        user = User.verify_auth_token(email_or_token)
        if not user:
            # try to authenticate with email/password
            user = User.query.filter_by(email=email_or_token).first()
            if not user or not user.verify_password(password):
                return False
        g.user = user
        return True
