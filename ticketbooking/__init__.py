from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:%s@localhost/flight_ticket_booking_system?charset=utf8mb4' % quote('matkhauoday')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app=app)
