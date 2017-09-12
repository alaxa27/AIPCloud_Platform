from .. import db
from time import time

class Query(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    point_id = db.Column(db.Integer, db.ForeignKey('access_points.id'))
    timestamp = db.Column(db.Integer, default = int(time()))
    exec_time = db.Column(db.Float)
    request = db.Column(db.String(10000))
    response = db.Column(db.String(10000))
    ip_address = db.Column(db.String(20))
