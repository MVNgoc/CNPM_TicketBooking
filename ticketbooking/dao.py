import json
from ticketbooking import app, login, db
from models import Account
import hashlib
from sqlalchemy import create_engine


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
    temp = Account.query.filter_by(userName=username.strip(), password=password).first()
    print(temp)
    return Account.query.filter_by(userName=username.strip(), password=password).first()


def get_user_by_username(id):
    return Account.query.filter_by(id=id).first()


def register_user(user_name, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    account = Account(userName=user_name, password=password,userRole='Customer')
    temp = db.session.add(account)
    if(temp):
        db.session.commit()
        return account
    else:
        return 'false'
