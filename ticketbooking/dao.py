import json
from ticketbooking import app, db
from models import Account, Invoice, Airport, Route, Flight, Price, SystemRule
import hashlib
from sqlalchemy.exc import IntegrityError
from sqlalchemy import cast, Date
from flask_login import current_user
from datetime import datetime, timedelta, timezone
from sqlalchemy import desc


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
    password = str(hashlib.md5(password.strip().encode('utf-8'))).hexdigest()
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


def load_list_of_ticket(account_id=None, kw=None):
    if current_user.is_authenticated:
        # Lấy mã hóa đơn theo user_id
        account_id = current_user.id
        query = Invoice.query.filter_by(accountID=account_id)
    else:
        query = Invoice.query

    if kw:
        query = query.filter(Invoice.invoiceID.contains(kw))

    # Sắp xếp theo thời gian tạo, từ mới nhất đến cũ nhất
    query = query.order_by(desc(Invoice.paymentTime))

    return query.all()


def load_list_of_airports():
    return Airport.query.all()


def load_route_of_airports(departure_point, destination):
    return Route.query.filter_by(departureAirportID=departure_point, arrivalAirportID=destination).first()


def load_flight_of_airports(routeID, time):
    # Lấy thời gian hiện tại
    current_time = datetime.now(timezone.utc)
    # Xác định thời điểm cách đây 12 tiếng
    twelve_hours_later = current_time + timedelta(hours=12)

    return Flight.query.filter_by(routeID=routeID).filter(
        cast(Flight.departureTime, Date) == time,
        Flight.departureTime >= twelve_hours_later).all()


def get_price_ticket(flightID):
    return Price.query.filter_by(flightID=flightID).all()

def load_booking_time():
    current_time = datetime.now().time()
    start_time = SystemRule.query.first().ticketBookingTime_Start
    end_time = SystemRule.query.first().ticketBookingTime_End

    if start_time <= current_time <= end_time:
        return 'booking_time_true'
    else:
        return 'booking_time_false'