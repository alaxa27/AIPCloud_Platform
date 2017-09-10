from .models import User, AccessPoint, Authorization
from time import time

class InitializeDB(object):

    def __init__(self, db):
        # Create the database
        db.create_all()
        # Add 2 users
        user1 = User(email='text@jdc.fr', admin=True)
        user1.hash_password('jdc')
        user2 = User(email='image@jdc.fr')
        user2.hash_password('jdc')
        user3 = User(email='admin@jdc.fr', admin=True)
        user3.hash_password('jdc')
        user4 = User(email='client@jdc.fr')
        user4.hash_password('jdc')
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.add(user4)
        db.session.commit()
        # Add access points to the data base
        paths = ['/analyze/word',
                 '/analyze/sentence',
                 '/analyze/text',
                 '/analyze/customer',
                 '/analyze/dialogue',
                 '/analyze/extraction',
                 '/analyze/image',
                 '/analyze/intent']
        for path in paths:
            if path == '/analyze/dialogue':
                db.session.add(AccessPoint(path=path, method='GET'))
            else:
                db.session.add(AccessPoint(path=path))
            db.session.commit()
        # Grant access to text methods for the first and the fourth users and for the admin
        l = paths[:-1]
        for path in l:
            ap = AccessPoint.query.filter_by(path=path).first()
            user1.grant_access_to(ap)
            user3.grant_access_to(ap)
            user4.grant_access_to(ap)
        # Grant access to image method for the second user and for the admin
        ap = AccessPoint.query.filter_by(path='/analyze/image').first()
        user2.grant_access_to(ap)
        user3.grant_access_to(ap)
