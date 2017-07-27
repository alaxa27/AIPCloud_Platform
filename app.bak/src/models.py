from . import app, db
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))
    access = db.relationship('UserAccess', backref='user', lazy='dynamic')
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration):
            s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
            return s.dumps({'id': self.id})

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



class UserAccess(db.Model):
    __tablename__ = 'user_access'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(20), index=True)
    timeref = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
