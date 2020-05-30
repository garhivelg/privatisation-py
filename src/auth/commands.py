from app import manager, db
from .models import User, ROLE_ADMIN


@manager.command
def superuser(login=None, password=None):
    """
    Add superuser
    :param login:
    :param password:
    :return:
    """
    if not login or not password:
        print("Login and password are required")
        return
    if User.query.filter_by(login=login).count():
        print("Login must be unique")
        return
    user = User(
        login=login,
        role=ROLE_ADMIN,
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    print("Superuser \"{}\" created".format(login))
