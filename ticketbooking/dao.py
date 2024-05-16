import json
from ticketbooking import app, db
from ticketbooking.models import Account, Invoice, Airport, Route, Flight, Price, SystemRule, Ticket, Customer
import hashlib
from sqlalchemy.exc import IntegrityError
from sqlalchemy import cast, Date, func, extract
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


# Luồng login, register
def auth_user_customer(username, password):  # Login
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = Account.query.filter_by(userName=username.strip(), password=password).first()
    if user and (user.userRole == 'Customer' or user.userRole == 'Employee'):
        return user
    else:
        return 'login_failed'


def get_user_by_username(id):
    return Account.query.filter_by(id=id).first()


def register_user(user_name, password):  # Register
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


def load_current_user():  # Đè authen cho mỗi trang
    if current_user.is_authenticated:
        return 'true'
    else:
        return 'false'


# Xử lý trang flight lookup
def load_list_of_airports():  # Lấy danh sách sân bay
    return Airport.query.all()


def load_route_of_airports(departure_point, destination):  # Lấy danh sách route
    return Route.query.filter_by(departureAirportID=departure_point, arrivalAirportID=destination).first()


def load_flight_of_airports(routeID, time):  # Lấy danh sách chuyến bay
    # Lấy thời gian hiện tại
    current_time = datetime.now(timezone.utc)
    # Xác định thời điểm cách đây 12 tiếng
    twelve_hours_later = current_time + timedelta(hours=12)

    return Flight.query.filter_by(routeID=routeID).filter(
        cast(Flight.departureTime, Date) == time,
        Flight.departureTime >= twelve_hours_later).all()


def get_price_ticket(flightID):  # Lấy giá vé theo từng chuyến bay
    return Price.query.filter_by(flightID=flightID).all()


def load_booking_time():  # Lấy thời gian đặt vé
    current_time = datetime.now().time()
    start_time = SystemRule.query.first().ticketBookingTime_Start
    end_time = SystemRule.query.first().ticketBookingTime_End

    if start_time <= current_time <= end_time:
        return 'booking_time_true'
    else:
        return 'booking_time_false'


# Luồng xử lý thêm data xuống database
def add_customer(list_info_user, quantity):
    list_customer_id = []  # Lấy ra danh sách khách hàng được nhập từ form
    try:
        for i in range(int(quantity)):  # Bắt đầu từ 0 đến số lượng nhập vào
            customer = Customer(customerName=list_info_user['customerName'][i], gender=list_info_user['sex'][i],
                                birthDate=datetime.strptime(list_info_user['birthdate'][i], '%m/%d/%Y'),
                                idNumber=list_info_user['idNumber'][i],
                                phoneNumber=list_info_user['phoneNumber'][i])
            db.session.add(customer)
            db.session.flush()  # Đảm bảo ID của khách hàng được tạo ra trước khi commit
            list_customer_id.append(customer.customerID)
        db.session.commit()

    except IntegrityError as e:
        db.session.rollback()
        return 'add_customer_false'

    return list_customer_id


def add_invoice(paymentAmount, transferImage):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    account_id = current_user.id
    invoice = Invoice(accountID=int(account_id), paymentAmount=float(paymentAmount), paymentStatus='Pending',
                      paymentMethod='BankTransfer', transferImage=transferImage,
                      paymentTime=current_time)

    db.session.add(invoice)
    db.session.commit()
    return invoice


def add_ticket(invoiceID, customerID, flightSelectInfo, type_ticket):
    account_id = current_user.id
    try:
        for i in customerID:  # Bao nhiêu khách hàng thì bấy nhiêu vé
            ticket = Ticket(invoiceID=int(invoiceID), customerID=int(i), accountID=int(account_id),
                            flightID=flightSelectInfo['flightID'], classID=flightSelectInfo['classID'],
                            priceID=flightSelectInfo['priceID'])  # Case một chiều
            db.session.add(ticket)

            if type_ticket == 'two-way':  # Case khứ hồi
                ticket_return = Ticket(invoiceID=int(invoiceID), customerID=int(i), accountID=int(account_id),
                                       flightID=flightSelectInfo['flightReturnID'],
                                       classID=flightSelectInfo['classReturnID'],
                                       priceID=flightSelectInfo['priceReturnID'])
                db.session.add(ticket_return)

        db.session.commit()

    except IntegrityError as e:
        db.session.rollback()
        return 'add_ticket_failed'

    return 'add_ticket_success'


# Luồng danh sách vé
def load_list_of_ticket(account_id=None, kw=None):  # Hiển thị danh sách vé
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


def load_invoice(invoice_id):  # Hiển thị chi tiết vé
    invoice = Invoice.query.filter_by(invoiceID=invoice_id).first()
    return invoice


def load_tickets(invoice_id):
    tickets = Ticket.query.filter_by(invoiceID=invoice_id).all()
    return tickets


def load_customers(invoice_id):
    ticket_customer_ids = [ticket.customerID for ticket in Ticket.query.filter_by(invoiceID=invoice_id).all()]
    customers = Customer.query.filter(Customer.customerID.in_(ticket_customer_ids)).all()
    return customers


def cancel_invoice(invoice_id):
    try:
        invoice = Invoice.query.filter_by(invoiceID=invoice_id).first()
        if invoice:
            invoice.paymentStatus = 'Cancelled'
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        print(f"Error cancelling invoice: {e}")
        return False


# code cho phần admin
def auth_user_admin(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = Account.query.filter_by(userName=username.strip(), password=password, userRole='Admin').first()
    if user:
        return user
    else:
        return 'login_failed'


def get_revenue_data_by_month(month, year):
    revenue_data = db.session.query(
        Route.routeID,
        Route.routeName,
        func.count(Flight.flightID).label('num_of_flights'),
        func.sum(Invoice.paymentAmount).label('total_revenue')
    ).join(Flight, Route.routeID == Flight.routeID
           ).join(Ticket, Ticket.flightID == Flight.flightID
                  ).join(Invoice, Invoice.invoiceID == Ticket.invoiceID
                         ).filter(
        extract('year', Invoice.paymentTime) == year,
        extract('month', Invoice.paymentTime) == month,
        Invoice.paymentStatus == 'Paid'
    ).group_by(Route.routeID, Route.routeName).all()

    return revenue_data

# code cho phần employee
def load_employee():
    with open('%s/data/employee.json' % app.root_path, encoding='utf-8') as f:
        return json.load(f)


def load_selling_time():
    current_time = datetime.now().time()
    start_time = SystemRule.query.first().ticketSaleTime_Start
    end_time = SystemRule.query.first().ticketSaleTime_End

    if start_time <= current_time <= end_time:
        return 'selling_time_true'
    else:
        return 'selling_time_false'


def add_invoice_employee(paymentAmount):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    account_id = current_user.id
    invoice = Invoice(accountID=int(account_id), paymentAmount=float(paymentAmount), paymentStatus='Paid',
                      paymentMethod='Cash', transferImage=None,
                      paymentTime=current_time)

    db.session.add(invoice)
    db.session.commit()
    return invoice


def load_flight_of_airports_employee(routeID, time):  # Lấy danh sách chuyến bay
    # Lấy thời gian hiện tại
    current_time = datetime.now(timezone.utc)
    # Xác định thời điểm cách đây 4 tiếng
    twelve_hours_later = current_time + timedelta(hours=4)

    return Flight.query.filter_by(routeID=routeID).filter(
        cast(Flight.departureTime, Date) == time,
        Flight.departureTime >= twelve_hours_later).all()

def add_flight_employee(flightID, routeID, departureTime, arrivalTime, numFirstClassSeat, numSecondClassSeat):
    total_Seat= numFirstClassSeat + numSecondClassSeat
    flight = Flight(flightID=flightID, routeID=routeID, departureTime=departureTime,arrivalTime=arrivalTime,
                    numOf1stClassSeat=numFirstClassSeat, numOf2ndClassSeat=numSecondClassSeat,flightStatus='Scheduled',
                    availableSeats=total_Seat)
    db.session.add(flight)
    db.session.commit()


def load_pending_bank_transfer_tickets():
    invoices = Invoice.query.filter_by(paymentMethod='BankTransfer',
                                      paymentStatus='Pending').all()
    return invoices


def approve_invoice(invoice_id):
    try:
        invoice = Invoice.query.filter_by(invoiceID=invoice_id).first()
        if invoice:
            invoice.paymentStatus = 'Paid'
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        print(f"Error cancelling invoice: {e}")
        return False