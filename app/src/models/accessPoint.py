from .. import db

class AccessPoint(db.Model):
    __tablename__ = 'access_points'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(100), index=True)
    method = db.Column(db.String(6), default = 'POST')
    users = db.relationship("Authorization", backref='point', lazy='dynamic')
