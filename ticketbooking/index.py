import datetime
from functools import wraps
from math import ceil

from flask import Flask, session, jsonify, url_for, render_template, request, redirect
from ticketbooking import app, dao, login
from flask_login import login_user, logout_user, current_user
import cloudinary.uploader
from admin import admin


# Luồng register, login, logout cho customer
@app.route('/')
def index():
    path = request.path
    categories = dao.load_categories()
    return render_template('customer/index.html', categories=categories, path=path)


@app.route('/', methods=['post'])
def process_login():
    username = request.form.get('username')
    password = request.form.get('pswd')
    u = dao.auth_user_customer(username=username, password=password)
    if u == 'login_failed':
        return render_template('customer/index.html', error_code=u)
    else:
        login_user(user=u)
        if u.userRole == 'Customer':
            return redirect('/')
        elif u.userRole == 'Employee':
            return redirect('/employee')


@app.route('/register', methods=['post'])
def process_register():
    username = request.form.get('username')
    password = request.form.get('passwordInput')
    u = dao.register_user(user_name=username, password=password)
    if u == 'account_already_exists':
        return render_template('customer/index.html', error_code=u)
    elif u == 'create_account_false':
        return render_template('customer/index.html', error_code=u)
    else:
        login_user(user=u)
        return redirect('/')


@login.user_loader
def load_user(id):
    return dao.get_user_by_username(id)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


# Luồng tra cứu vé
@app.route('/flight-lookup')  # Load data lên trang
def flight_lookup():
    path = request.path
    categories = dao.load_categories()
    list_airports = dao.load_list_of_airports()

    booking_allowed = dao.load_booking_time()
    authen = dao.load_current_user()

    if authen == 'true':
        if booking_allowed == 'booking_time_true':
            return render_template('customer/flightlookuplayout/flight_lookup.html', categories=categories, path=path,
                                   list_airports=list_airports, booking_allowed=booking_allowed)
        if booking_allowed == 'booking_time_false':
            return render_template('customer/flightlookuplayout/flight_lookup.html', categories=categories, path=path,
                                   error_code=booking_allowed)
    else:
        return redirect('/')


@app.route('/flight-lookup/select-flight')  # Load trang chọn vé
def select_flight():
    path = request.path
    categories = dao.load_categories()
    bookticketstep = dao.load_book_ticket_step()

    authen = dao.load_current_user()

    if authen == 'true':
        return render_template('customer/flightlookuplayout/select_flight.html', categories=categories, path=path,
                               bookticketstep=bookticketstep)
    else:
        return redirect('/')


@app.route('/flight-lookup/select-flight', methods=['post'])  # Lấy thông tin user tra cứu, tra cứu dưới db
def process_select_flight():
    path = request.path
    categories = dao.load_categories()
    bookticketstep = dao.load_book_ticket_step()

    departure_point = request.form.get('departure_point').split('-')
    destination = request.form.get('destination').split('-')
    date_of_department = request.form.get('date_of_department')
    quantity = request.form.get('quantity')
    type_ticket = request.form.get('type_ticket')
    # Tạo mảng để lưu danh sách vé
    flight_list_format = []
    return_flight_list_format = []
    # Lấy danh sách route tương ứng
    route = dao.load_route_of_airports(departure_point[0], destination[0])
    return_route = dao.load_route_of_airports(destination[0], departure_point[0])

    # Lấy danh sách các vé
    if type_ticket == 'two-way':
        returnDate = request.form['returnDate']
        if return_route:
            return_flight_list = dao.load_flight_of_airports(return_route.routeID, returnDate)
            for flight in return_flight_list:
                price_ticket = dao.get_price_ticket(flight.flightID)
                return_flight_list_format.append(
                    {
                        'flightID': flight.flightID,
                        'routeID': flight.routeID,
                        'departureTime': flight.departureTime,
                        'arrivalTime': flight.arrivalTime,
                        'numOf1stClassSeat': flight.numOf1stClassSeat,
                        'numOf2ndClassSeat': flight.numOf2ndClassSeat,
                        'flightStatus': flight.flightStatus,
                        'availableSeats': flight.availableSeats,
                        'price': price_ticket
                    })
        else:
            return_flight_list_format = []

    if route:
        flight_list = dao.load_flight_of_airports(route.routeID, date_of_department)
        for flight in flight_list:
            price_ticket = dao.get_price_ticket(flight.flightID)
            flight_list_format.append(  # Thêm ticket lần lượt vào cuối danh sách
                {
                    'flightID': flight.flightID,
                    'routeID': flight.routeID,
                    'departureTime': flight.departureTime,
                    'arrivalTime': flight.arrivalTime,
                    'numOf1stClassSeat': flight.numOf1stClassSeat,
                    'numOf2ndClassSeat': flight.numOf2ndClassSeat,
                    'flightStatus': flight.flightStatus,
                    'availableSeats': flight.availableSeats,
                    'price': price_ticket
                })
    else:
        flight_list_format = []  # Trả ra rỗng

    session['flight_info'] = {  # Lưu vào session
        'departure_point': departure_point,
        'destination': destination,
        'type_ticket': type_ticket,
        'quantity': int(quantity),
    }

    return render_template('customer/flightlookuplayout/select_flight.html', categories=categories, path=path,
                           bookticketstep=bookticketstep, flight_list_format=flight_list_format,
                           return_flight_list_format=return_flight_list_format)


@app.route('/flight-lookup/passengers', methods=['post'])  # Lấy thông tin thông tin khách nhập vào, lưu vào session
def process_passengers():
    path = request.path
    categories = dao.load_categories()
    bookticketstep = dao.load_book_ticket_step()

    quantity = int(session['flight_info']['quantity'])  # Lấy số lượng khách từ session

    if request.form.get('ticket_price'):  # Lấy giá tiền từ footer * quantity
        ticket_price = float(request.form.get('ticket_price')) * quantity
    else:
        ticket_price = 0

    if request.form.get('ticket_price_return'):
        ticket_price_return = float(request.form.get('ticket_price_return')) * quantity
    else:
        ticket_price_return = 0

    if request.form.get('total_ticket_price'):
        total_ticket_price = float(request.form.get('total_ticket_price')) * quantity
    else:
        total_ticket_price = 0

    session['ticket_price_info'] = {  # Lưu vào session
        'ticket_price': float(ticket_price) or 0,
        'ticket_price_return': float(ticket_price_return) or 0,
        'total_ticket_price': float(total_ticket_price) or 0,
    }

    # Lấy data vé đã chọn
    flightID = request.form.get('flightID')
    priceID = request.form.get('priceID')
    classID = request.form.get('classID')

    flightReturnID = request.form.get('flightReturnID')
    priceReturnID = request.form.get('priceReturnID')
    classReturnID = request.form.get('classReturnID')

    session['flight_select_info'] = {  # Lưu vào session
        'flightID': flightID,
        'priceID': priceID,
        'classID': classID,
        'flightReturnID': flightReturnID,
        'priceReturnID': priceReturnID,
        'classReturnID': classReturnID,
    }

    return render_template('customer/flightlookuplayout/passengers.html', categories=categories, path=path,
                           bookticketstep=bookticketstep, quantity=quantity)


@app.route('/flight-lookup/pay-ticket')
def pay_ticket():
    path = request.path
    categories = dao.load_categories()
    bookticketstep = dao.load_book_ticket_step()
    authen = dao.load_current_user()

    payment_status = request.args.get('payment')  # Hiện popup

    if authen == 'true':
        return render_template('customer/flightlookuplayout/pay_ticket.html', categories=categories, path=path,
                               bookticketstep=bookticketstep, payment_status=payment_status)
    else:
        return redirect('/')


@app.route('/flight-lookup/pay-ticket', methods=['post'])  # Lưu danh sách các customer vào bảng customer
def process_pay_ticket():
    path = request.path
    categories = dao.load_categories()
    bookticketstep = dao.load_book_ticket_step()

    customerName = request.form.getlist('customerName')
    sex = request.form.getlist('sex')
    birthdate = request.form.getlist('birthdate')
    idNumber = request.form.getlist('idNumber')
    phoneNumber = request.form.getlist('phoneNumber')

    session['passengers'] = {
        'customerName': customerName,
        'sex': sex,
        'birthdate': birthdate,
        'idNumber': idNumber,
        'phoneNumber': phoneNumber,
    }  # Lấy thông tin các passenger từ session

    return render_template('customer/flightlookuplayout/pay_ticket.html', categories=categories, path=path,
                           bookticketstep=bookticketstep)


@app.route('/flight-lookup/pay-ticket-upload', methods=['post'])  # Lưu invoice, ticket vào database
def process_pay_ticket_upload():
    image = request.files['image']
    res = cloudinary.uploader.upload(image)
    url_image = res['secure_url']  # Lấy hình, đẩy hình lên cloud, lấy link hình sau khi được upload trên cloud

    if url_image:
        customer_id = dao.add_customer(session['passengers'], session['flight_info']['quantity'])
        invoice_id = dao.add_invoice(session['ticket_price_info']['total_ticket_price'], url_image).invoiceID
        res_add_ticket = dao.add_ticket(invoice_id, customer_id, session['flight_select_info'],
                                        session['flight_info']['type_ticket'])
        if res_add_ticket == 'add_ticket_success':
            return redirect('/flight-lookup/pay-ticket?payment=success')
        else:
            return redirect('/flight-lookup/pay-ticket?payment=failure')
    else:
        return redirect('/flight-lookup/pay-ticket?payment=failure')


@app.route('/tickets-booked')
def tickets_booked():
    authen = dao.load_current_user()

    if authen == 'true':
        path = request.path
        categories = dao.load_categories()
        kw = request.args.get('keyword')
        account_id = current_user.id
        invoices = dao.load_list_of_ticket(account_id=account_id, kw=kw)
        total_invoices = len(invoices)  # Tổng số hóa đơn
        per_page = 5  # Số lượng hóa đơn muốn hiển thị trên mỗi trang
        page = request.args.get('page', 1, type=int)
        num_pages = ceil(total_invoices / per_page)  # Tính số trang
        start_index = (page - 1) * per_page
        end_index = min(start_index + per_page, total_invoices)
        invoices_on_page = invoices[start_index:end_index]

        return render_template('customer/listofticket/tickets_booked.html', categories=categories, path=path,
                               invoices=invoices_on_page, page=page, num_pages=num_pages)
    else:
        return redirect('/')


@app.route('/tickets-booked/tickets-booked-details/<int:invoice_id>')
def tickets_booked_details(invoice_id):
    path = request.path
    categories = dao.load_categories()
    listofticketstep = dao.load_list_of_ticket_step()
    authen = dao.load_current_user()

    if authen == 'true':
        invoice = dao.load_invoice(invoice_id)
        tickets = dao.load_tickets(invoice_id)
        customers = dao.load_customers(invoice_id)
        total_amount = invoice.paymentAmount
        payment_status = invoice.paymentStatus

        return render_template('customer/listofticket/tickets_booked_details.html', categories=categories, path=path,
                               listofticketstep=listofticketstep, invoice=invoice, tickets=tickets, customers=customers,
                               total_amount=total_amount, payment_status=payment_status, invoice_id=invoice_id)
    else:
        return redirect('/')


@app.route('/cancel-invoice/<int:invoice_id>', methods=['GET', 'POST'])
def cancel_invoice_route(invoice_id):
    dao.cancel_invoice(invoice_id)
    return redirect('/tickets-booked')


# code cho phần admin
@app.route('/login-admin', methods=['post'])
def admin_login():
    username = request.form['username']
    password = request.form['pswd']

    user = dao.auth_user_admin(username=username,
                               password=password)
    if user == 'login_failed':
        return render_template('customer/index.html', error_code=user)
    else:
        login_user(user=user)
    return redirect('/admin')


@app.context_processor
def common_atstr():
    categories = dao.load_categories()
    return {
        'categories': categories
    }


# code cho phần employee
def employee_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.userRole != 'Employee':
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function


@app.route('/employee')
@employee_required
def employee_index():
    path = request.path
    categories = dao.load_employee()
    return render_template('employee/index.html', categories=categories, path=path)


@app.route('/employee/flight-lookup')
@employee_required
def employee_flight_lookup():
    path = request.path
    categories = dao.load_employee()
    list_airports = dao.load_list_of_airports()
    selling_allowed = dao.load_selling_time()

    if selling_allowed == 'selling_time_true':
        return render_template('employee/flightlookuplayout/flight_lookup.html', categories=categories, path=path,
                               list_airports=list_airports, selling_allowed=selling_allowed)
    else:
        return render_template('employee/flightlookuplayout/flight_lookup.html', categories=categories, path=path,
                               error_code=selling_allowed)


@app.route('/employee/flight-lookup/select-flight')
@employee_required
def employee_select_flight():
    path = request.path
    categories = dao.load_employee()
    bookticketstep = dao.load_book_ticket_step()
    return render_template('employee/flightlookuplayout/select_flight.html', categories=categories, path=path,
                           bookticketstep=bookticketstep)


@app.route('/employee/flight-lookup/select-flight', methods=['post'])
@employee_required
def employee_process_select_flight():
    path = request.path
    categories = dao.load_employee()
    bookticketstep = dao.load_book_ticket_step()

    departure_point = request.form.get('departure_point').split('-')
    destination = request.form.get('destination').split('-')
    date_of_department = request.form.get('date_of_department')
    quantity = request.form.get('quantity')
    type_ticket = request.form.get('type_ticket')
    flight_list_format = []
    return_flight_list_format = []

    route = dao.load_route_of_airports(departure_point[0], destination[0])
    return_route = dao.load_route_of_airports(destination[0], departure_point[0])

    if type_ticket == 'two-way':
        returnDate = request.form['returnDate']
        if return_route:
            return_flight_list = dao.load_flight_of_airports_employee(return_route.routeID, returnDate)
            for flight in return_flight_list:
                price_ticket = dao.get_price_ticket(flight.flightID)
                return_flight_list_format.append(
                    {
                        'flightID': flight.flightID,
                        'routeID': flight.routeID,
                        'departureTime': flight.departureTime,
                        'arrivalTime': flight.arrivalTime,
                        'numOf1stClassSeat': flight.numOf1stClassSeat,
                        'numOf2ndClassSeat': flight.numOf2ndClassSeat,
                        'flightStatus': flight.flightStatus,
                        'availableSeats': flight.availableSeats,
                        'price': price_ticket
                    })
        else:
            return_flight_list_format = []

    if route:
        flight_list = dao.load_flight_of_airports_employee(route.routeID, date_of_department)
        for flight in flight_list:
            price_ticket = dao.get_price_ticket(flight.flightID)
            flight_list_format.append(
                {
                    'flightID': flight.flightID,
                    'routeID': flight.routeID,
                    'departureTime': flight.departureTime,
                    'arrivalTime': flight.arrivalTime,
                    'numOf1stClassSeat': flight.numOf1stClassSeat,
                    'numOf2ndClassSeat': flight.numOf2ndClassSeat,
                    'flightStatus': flight.flightStatus,
                    'availableSeats': flight.availableSeats,
                    'price': price_ticket
                })
    else:
        flight_list_format = []

    session['flight_info'] = {
        'departure_point': departure_point,
        'destination': destination,
        'type_ticket': type_ticket,
        'quantity': int(quantity),
    }

    return render_template('employee/flightlookuplayout/select_flight.html', categories=categories, path=path,
                           bookticketstep=bookticketstep, flight_list_format=flight_list_format,
                           return_flight_list_format=return_flight_list_format)


@app.route('/employee/flight-lookup/passengers', methods=['post'])
@employee_required
def employee_process_passengers():
    path = request.path
    categories = dao.load_employee()
    bookticketstep = dao.load_book_ticket_step()

    quantity = int(session['flight_info']['quantity'])

    if request.form.get('ticket_price'):  # Lấy giá tiền từ footer
        ticket_price = float(request.form.get('ticket_price')) * quantity
    else:
        ticket_price = 0

    if request.form.get('ticket_price_return'):
        ticket_price_return = float(request.form.get('ticket_price_return')) * quantity
    else:
        ticket_price_return = 0

    if request.form.get('total_ticket_price'):
        total_ticket_price = float(request.form.get('total_ticket_price')) * quantity
    else:
        total_ticket_price = 0

    session['ticket_price_info'] = {
        'ticket_price': float(ticket_price) or 0,
        'ticket_price_return': float(ticket_price_return) or 0,
        'total_ticket_price': float(total_ticket_price) or 0,
    }

    # Lấy data vé đã chọn
    flightID = request.form.get('flightID')
    priceID = request.form.get('priceID')
    classID = request.form.get('classID')

    flightReturnID = request.form.get('flightReturnID')
    priceReturnID = request.form.get('priceReturnID')
    classReturnID = request.form.get('classReturnID')

    session['flight_select_info'] = {
        'flightID': flightID,
        'priceID': priceID,
        'classID': classID,
        'flightReturnID': flightReturnID,
        'priceReturnID': priceReturnID,
        'classReturnID': classReturnID,
    }

    return render_template('employee/flightlookuplayout/passengers.html', categories=categories, path=path,
                           bookticketstep=bookticketstep, quantity=quantity)


@app.route('/employee/flight-lookup/pay-ticket')
@employee_required
def employee_pay_ticket():
    path = request.path
    categories = dao.load_employee()
    bookticketstep = dao.load_book_ticket_step()
    payment_status = request.args.get('payment')

    return render_template('employee/flightlookuplayout/pay_ticket.html', categories=categories, path=path,
                           bookticketstep=bookticketstep, payment_status=payment_status)


@app.route('/employee/flight-lookup/pay-ticket', methods=['post'])
@employee_required
def employee_process_pay_ticket():
    path = request.path
    categories = dao.load_employee()
    bookticketstep = dao.load_book_ticket_step()

    customer_id = dao.add_customer(session['passengers'], session['flight_info']['quantity'])
    invoice_id = dao.add_invoice_employee(session['ticket_price_info']['total_ticket_price']).invoiceID
    add_ticket = dao.add_ticket(invoice_id, customer_id, session['flight_select_info'],
                                    session['flight_info']['type_ticket'])

    if add_ticket == 'add_ticket_success':
        return redirect('/employee/flight-lookup')
    else:
        return redirect('/employee/flight-lookup/pay-ticket')


@app.route('/employee/tickets-booked')
@employee_required
def employee_tickets_booked():
    path = request.path
    categories = dao.load_employee()
    kw = request.args.get('keyword')
    account_id = current_user.id
    invoices = dao.load_list_of_ticket(account_id=account_id, kw=kw)
    total_invoices = len(invoices)  # Tổng số hóa đơn
    per_page = 5  # Số lượng hóa đơn muốn hiển thị trên mỗi trang
    page = request.args.get('page', 1, type=int)
    num_pages = ceil(total_invoices / per_page)  # Tính số trang
    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, total_invoices)
    invoices_on_page = invoices[start_index:end_index]

    return render_template('employee/listofticket/tickets_booked.html', categories=categories, path=path,
                           invoices=invoices_on_page, page=page, num_pages=num_pages)


@app.route('/employee/tickets-booked/tickets-booked-details/<int:invoice_id>')
@employee_required
def employee_tickets_booked_details(invoice_id):
    path = request.path
    categories = dao.load_employee()
    listofticketstep = dao.load_list_of_ticket_step()
    invoice = dao.load_invoice(invoice_id)
    tickets = dao.load_tickets(invoice_id)
    customers = dao.load_customers(invoice_id)
    total_amount = invoice.paymentAmount
    payment_status = invoice.paymentStatus

    return render_template('employee/listofticket/tickets_booked_details.html', categories=categories, path=path,
                           listofticketstep=listofticketstep, invoice=invoice, tickets=tickets, customers=customers,
                           total_amount=total_amount, payment_status=payment_status, invoice_id=invoice_id)


@app.route('/employee/cancel-invoice/<int:invoice_id>', methods=['GET', 'POST'])
@employee_required
def employee_cancel_invoice_route(invoice_id):
    dao.cancel_invoice(invoice_id)
    return redirect('/employee/tickets-booked')


@app.route('/employee/add-flight', methods=['GET', 'POST'])
@employee_required
def employee_add_flight():
    if request.method == 'POST':
        flightID = request.form.get('flightCode')
        routeID = request.form.get('routeCode')
        departureTime = request.form.get('departureTime')
        arrivalTime = request.form.get('arrivalTime')
        numFirstClassSeat = int(request.form.get('seatClass1'))
        numSecondClassSeat = int(request.form.get('seatClass2'))

        dao.add_flight_employee(flightID, routeID, departureTime, arrivalTime, numFirstClassSeat, numSecondClassSeat)

        return redirect('/employee')
    else:
        path = request.path
        categories = dao.load_employee()
        return render_template('employee/addflight/add-flight.html', categories=categories, path=path)


@app.route('/employee/approve-invoice')
@employee_required
def employee_approve_invoice():
    path = request.path
    categories = dao.load_employee()
    invoices = dao.load_pending_bank_transfer_tickets()

    return render_template('employee/approveinvoice/approve_invoice.html', categories=categories, path=path,
                           invoices=invoices)


@app.route('/employee/approve-invoice/cancel-invoice/<int:invoice_id>')
@employee_required
def employee_cancel_invoice(invoice_id):
    dao.cancel_invoice(invoice_id)
    return redirect('/employee/approve-invoice')


@app.route('/employee/approve-invoice/confirm-invoice/<int:invoice_id>')
@employee_required
def employee_confirm_approve_invoice(invoice_id):
    dao.approve_invoice(invoice_id)
    return redirect('/employee/approve-invoice')


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)