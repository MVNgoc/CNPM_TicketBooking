from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/flight_ticket_booking_system?charset=utf8mb4' % quote(
    '123456')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = '!@@!#@!#!@sdkjfasdadhadkhdjahdsaldha!@#!@#@!#@!'

cloudinary.config(cloud_name='dolvkgnba', api_key='331598661687368', api_secret='JJREe6YqJv2XKYLYxaZqyP9xpOA')

db = SQLAlchemy(app=app)

login = LoginManager(app)