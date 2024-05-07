from flask import render_template, request, redirect
from flask import Flask
from ticketbooking import app, dao, login
from flask_login import login_user, logout_user


@app.route('/')
def index():
    path = request.path
    categories = dao.load_categories()
    return render_template('index.html', categories=categories, path=path)


@app.route('/', methods=['post'])
def process_login():
    username = request.form.get('username')
    password = request.form.get('pswd')
    u = dao.auth_user(username=username, password=password)
    if u == 'login_failed':
        return render_template('index.html', error_code=u)
    else:
        login_user(user=u)
        return redirect('/flight-lookup')


@app.route('/register', methods=['post'])
def process_register():
    username = request.form.get('username')
    password = request.form.get('passwordInput')
    u = dao.register_user(user_name=username, password=password)
    if u == 'account_already_exists':
        return render_template('index.html', error_code=u)
    elif u == 'create_account_false':
        return render_template('index.html', error_code=u)
    else:
        login_user(user=u)
        return redirect('/flight-lookup')


@login.user_loader
def load_user(id):
    return dao.get_user_by_username(id)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/flight-lookup')
def flight_lookup():
    path = request.path
    categories = dao.load_categories()
    return render_template('flightlookuplayout/flight_lookup.html', categories=categories, path=path)


@app.route('/flight-lookup/select-flight')
def select_flight():
    path = request.path
    categories = dao.load_categories()
    bookticketstep = dao.load_book_ticket_step()
    return render_template('flightlookuplayout/select_flight.html', categories=categories, path=path,
                           bookticketstep=bookticketstep)


# @app.route('/flight-lookup/select-flight', methods=['post'])
# def process_select_flight():
#


@app.route('/flight-lookup/passengers')
def passengers():
    path = request.path
    categories = dao.load_categories()
    bookticketstep = dao.load_book_ticket_step()
    return render_template('flightlookuplayout/passengers.html', categories=categories, path=path,
                           bookticketstep=bookticketstep)


@app.route('/tickets-booked')
def tickets_booked():
    path = request.path
    categories = dao.load_categories()
    kw = request.args.get('keyword')
    invoice = dao.load_list_of_ticket(kw=kw)
    return render_template('listofticket/tickets_booked.html', categories=categories, path=path, invoice=invoice)


@app.route('/tickets-booked/tickets-booked-details')
def tickets_booked_details():
    path = request.path
    categories = dao.load_categories()
    listofticketstep = dao.load_list_of_ticket_step()
    return render_template('listofticket/tickets_booked_details.html', categories=categories, path=path,
                           listofticketstep=listofticketstep)


@app.route('/login')
def login():
    path = request.path
    categories = dao.load_categories()
    return render_template('login.html', categories=categories, path=path)


@app.route('/register')
def signin():
    path = request.path
    categories = dao.load_categories()
    return render_template('register.html', categories=categories, path=path)


@app.route('/flight-lookup/pay-ticket')
def pay_ticket():
    path = request.path
    categories = dao.load_categories()
    bookticketstep = dao.load_book_ticket_step()
    return render_template('flightlookuplayout/pay_ticket.html', categories=categories, path=path,
                           bookticketstep=bookticketstep)


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
