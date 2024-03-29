from .. import app, db
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context
from flask import abort, request
from time import time

from .authorization import Authorization
from .accessPoint import AccessPoint
from .query import Query

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.Text)
    admin = db.Column(db.Boolean, default=False)
    test = db.Column(db.Boolean, default=False)
    queries_max = db.Column(db.Integer, default=-1)
    points = db.relationship("Authorization", backref='user', lazy='joined', cascade='all,delete')

    def authorization_exists(self, point):
        with db.session.no_autoflush:
            return Authorization.query.filter_by(user_id = self.id, point_id = point.id).first()

    def save(self):
        db.session.commit()

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        while Authorization.query.filter_by(user_id = self.id).first() is not None:
            auth = Authorization.query.filter_by(user_id = self.id).first()
            auth.delete()

        db.session.delete(self)
        db.session.commit()

    def set_queries_max(self, queries_max):
        if type(queries_max) is int:
            self.queries_max = queries_max
            db.session.commit()
        else:
            return False

    def adminify(self):
        self.admin = True
        db.session.commit()

    def deadminify(self):
        self.admin = False
        db.session.commit()

    def grant_access_to(self, point, timeref=None):
        if point is None:
            raise Exception('This access point does not exist.')
        auth = self.authorization_exists(point)
        if timeref is None:
            timeref = int(time()) + 86400
        timeref = int(timeref)
        if auth:
            auth.timeref = timeref
            db.session.commit()
            return True
        else:
            auth = Authorization(timeref = timeref)
            auth.point = point
            self.points.append(auth)
            db.session.commit()
            return False

    def unauthorize(self, point):
        self.points.remove(point)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    def verify_access(self, path):
        if not self.admin:
            if self.test == 1:
                queries_number = Query.query.filter_by(user_id = self.id, ip_address=request.environ['REMOTE_ADDR']).count()
                if queries_number >= self.queries_max:
                    abort(403, 'You have exceeded the maximum number of queries permitted. Please contact JDC for more information.')
            else:
                queries_number = Query.query.filter_by(user_id = self.id).count()
                if self.queries_max != -1 and queries_number >= self.queries_max:
                    abort(403, 'You have exceeded the maximum number of queries permitted. Please contact JDC for more information.')
                point = AccessPoint.query.filter_by(path=path).first()
                auths = self.points
                counter = 0
                for element in auths:
                    if element.point_id == point.id and element.timeref >= int(time()):
                        counter = 1
                if counter == 0:
                    abort(403)

    def save_query(self, path, data, exectime):
        point = AccessPoint.query.filter_by(path=path).first()
        db.session.add(Query(user_id=self.id,
                             point_id=point.id,
                             request=str(request.json),
                             response=str(data),
                             exec_time = exectime,
                             ip_address = request.environ['REMOTE_ADDR']))
        db.session.commit()

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
