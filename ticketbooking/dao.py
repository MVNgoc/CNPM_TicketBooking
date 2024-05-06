import json
from ticketbooking import app, login, db
from models import Account
import hashlib
from sqlalchemy.exc import IntegrityError


def load_categories():
    with open('%s/data/categories.json' % app.root_path, encoding='utf-8') as f:
        return json.load(f)


def load_book_ticket_step():
    with open('%s/data/bookticketstep.json' % app.root_path, encoding='utf-8') as f:
        return json.load(f)


def load_list_of_ticket_step():
    with open('%s/data/listofticketstep.json' % app.root_path, encoding='utf-8') as f:
        return json.load(f)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = Account.query.filter_by(userName=username.strip(), password=password).first()
    if user:
        return user
    else:
        return 'login_failed'


def get_user_by_username(id):
    return Account.query.filter_by(id=id).first()


def register_user(user_name, password):
    try:
        if Account.query.filter_by(userName=user_name).first() is not None:
            return 'account_already_exists'

        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        account = Account(userName=user_name, password=password, userRole='Customer')
        db.session.add(account)
        db.session.commit()

        account = Account.query.filter_by(userName=user_name).first()
        if account:
            return account
        else:
            return 'create_account_false'

    except IntegrityError as e:
        db.session.rollback()
        return 'create_account_false'
