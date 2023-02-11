import datetime
import uuid
from account import app, db, bcrypt
from account.models import User


def flaskrun():
    with app.app_context():
        db.create_all()
        # db.drop_all()
        app.run(debug=True)


def createsuperuser():
    username = input("Enter user name: ")
    email = input("Ener email: ")
    password = input("Enter password: ")
    user = User(username=username, email=email, password_hash=password, is_admin=True)
    with app.app_context():
        db.session.add(user)
        db.session.commit()
    print("Super User has been successfully created.")







# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()

#     app.run(debug=True)
