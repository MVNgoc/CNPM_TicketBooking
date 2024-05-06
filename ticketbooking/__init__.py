from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/flight_ticket_booking_system?charset=utf8mb4' % quote(
    '16102002Ly.')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = '!@@!#@!#!@sdkjfasdadhadkhdjahdsaldha!@#!@#@!#@!'
db = SQLAlchemy(app=app)

login = LoginManager(app)
