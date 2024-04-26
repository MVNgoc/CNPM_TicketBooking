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
    return render_template('flight_lookup.html', categories=categories, path=path)


@app.route('/tickets-booked')
def tickets_booked():
    path = request.path
    categories = dao.load_categories()
    return render_template('tickets_booked.html', categories=categories, path=path)


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
