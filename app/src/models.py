from . import app, db
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context
from flask import abort
from time import time


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(32))
    admin = db.Column(db.Boolean, default=False)
    points = db.relationship("Authorization", backref='user', lazy='dynamic')

    def grant_access_to(self, point):
        self.points.append(point)

    def unauthorize(self, point):
        self.ponts.remove(point)

    def hash_password(self, password):
        self.password_hash = password

    def verify_password(self, password):
        return password == self.password_hash

    def generate_auth_token(self, expiration):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    def verify_access(self, path):
        if not self.admin:
            point = AccessPoint.query.filter_by(path=path).first()
            auths = self.points
            counter = 0
            for element in auths:
                if element.point_id == point.id and element.timeref >= int(time()) - 86400:
                    counter = 1
            if counter == 0:
                abort(403)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user


class AccessPoint(db.Model):
    __tablename__ = 'access_points'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(20), index=True)
    users = db.relationship("Authorization", backref='point', lazy='dynamic')


class Authorization(db.Model):
    __tablename__ = 'authorizations'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    point_id = db.Column(db.Integer, db.ForeignKey('access_points.id'), primary_key=True)
    timeref = db.Column(db.Integer)
