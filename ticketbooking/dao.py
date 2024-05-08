import json
from ticketbooking import app, login, db
from models import Account, Invoice, Airport, Route, Flight
import hashlib
from sqlalchemy.exc import IntegrityError
from sqlalchemy import cast, Date
from flask_login import current_user


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


def get_account_id(username):
    if current_user.is_authenticated:
        return current_user.id
    else:
        return None


def load_list_of_ticket(account_id=None, kw=None, page=None):
    if current_user.is_authenticated:
        account_id = current_user.id
        query = Invoice.query.filter_by(accountID=account_id)
    else:
        query = Invoice.query

    if kw:
        query = query.filter(Invoice.invoiceID.contains(kw))

    return query.all()


def load_list_of_airports():
    return Airport.query.all()


def load_route_of_airports(departure_point, destination):
    return Route.query.filter_by(departureAirportID=departure_point, arrivalAirportID=destination).first()


def load_flight_of_airports(routeID, time):
    return Flight.query.filter_by(routeID=routeID).filter(
        cast(Flight.departureTime, Date) == time).all()
