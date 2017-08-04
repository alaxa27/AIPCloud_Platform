from .models import User, AccessPoint, Authorization
from time import time

class InitializeDB(object):

    def __init__(self, db):
        # Create the database
        db.create_all()
        # Add 2 users
        user1 = User(email='text@jdc.fr')
        user1.hash_password('jdc')
        user2 = User(email='image@jdc.fr')
        user2.hash_password('junior')
        user3 = User(email='admin@jdc.fr', admin=True)
        user3.hash_password('jdc')
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()
        # Add acces points to the data base
        paths = ['/analyze/sentence', '/analyze/text', '/analyze/customer', '/analyze/dialogue', '/analyze/extraction', '/image']
        for path in paths:
            db.session.add(AccessPoint(path=path))
            db.session.commit()
        # Grant access to text methods for the first user
        l = paths[:-1]
        for path in l:
            auth = Authorization(timeref=int(time()))
            ap = AccessPoint.query.filter_by(path=path).first()
            auth.point = ap
            user1.grant_access_to(auth)
            db.session.commit()
        # Grant access to image method for the second user
        auth = Authorization(timeref=int(time()))
        ap = AccessPoint.query.filter_by(path='/image').first()
        auth.point = ap
        user2.grant_access_to(auth)
        db.session.commit()
        # Grant access to all methods for the admin
        for path in paths:
            auth = Authorization(timeref=int(time()))
            ap = AccessPoint.query.filter_by(path=path).first()
            auth.point = ap
            user3.grant_access_to(auth)
            db.session.commit()
