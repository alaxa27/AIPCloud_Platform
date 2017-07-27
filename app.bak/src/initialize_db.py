from .models import User, UserAccess
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
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        # Grant access to text methods for the first user
        l = ['/analyze/sentence', '/analyze/text', '/analyze/customer']
        for path in l:
            db.session.add(UserAccess(path=path, timeref=int(time()), user=user1))
            db.session.commit()
        # Grant access to image method for the second user
        db.session.add(UserAccess(path='/image', timeref=int(time()), user=user2))
        db.session.commit()
