from flask import render_template, request
from flask import Flask
from ticketbooking import dao
from ticketbooking import app


@app.route('/')
def index():
    path = request.path
    categories = dao.load_categories()
    return render_template('index.html', categories=categories, path=path)


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


@app.route('/tickets-booked')
def tickets_booked():
    path = request.path
    categories = dao.load_categories()
    return render_template('ticketorder/tickets_booked.html', categories=categories, path=path)


@app.route('/tickets-booked/tickets-booked-details')
def tickets_booked_details():
    path = request.path
    categories = dao.load_categories()
    listofticketstep = dao.load_list_of_ticket_step()
    return render_template('ticketorder/tickets_booked_details.html', categories=categories, path=path,
                           listofticketstep=listofticketstep)


@app.route('/login')
def login():
    path = request.path
    categories = dao.load_categories()
    return render_template('login.html', categories=categories, path=path)


@app.route('/signin')
def signin():
    path = request.path
    categories = dao.load_categories()
    return render_template('signin.html', categories=categories, path=path)


@app.route('/flight-lookup/pay-ticket')
def pay_ticket():
    path = request.path
    categories = dao.load_categories()
    bookticketstep = dao.load_book_ticket_step()
    return render_template('flightlookuplayout/pay_ticket.html', categories=categories, path=path, bookticketstep=bookticketstep)


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)