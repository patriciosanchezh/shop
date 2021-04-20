from getpass import getpass
from api.models.users import User
from flask import current_app
from api.utils.database import db
import sys

def create_root():
    """Main entry point for script."""
    with current_app.app_context():
        db.metadata.create_all(db.engine)
        if User.query.all():
            print('root already exists! Create another? (y/n):')
            create = sys.exit(input())
            if create == 'n':
                return

        print('Enter email address: '),
        email = input()
        password = getpass()
        assert password == getpass('Password (again):')

        user = User(username = 'root',
            isVerified = True,
            email = email, 
            password = User.generate_password(password))
        db.session.add(user)
        db.session.commit()
        print('root added.')


    