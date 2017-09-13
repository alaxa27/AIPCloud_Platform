from .. import db

class Authorization(db.Model):
    __tablename__ = 'authorizations'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    point_id = db.Column(db.Integer, db.ForeignKey('access_points.id'), primary_key=True)
    timeref = db.Column(db.Integer)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
