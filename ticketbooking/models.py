from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from ticketbooking import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin

transit_airports_routes = Table(
    'transit_airports_routes',
    db.metadata,
    Column('airport_id', String(10), ForeignKey('airport.airportID'), primary_key=True),
    Column('route_id', String(10), ForeignKey('route.routeID'), primary_key=True)
)
class Airport(db.Model):
    __tablename__ = 'airport'
    airportID= Column(String(10), primary_key= True)
    airportName = Column(String(100), nullable= False)
    locationCity = Column(String(50))
    locationCountry = Column(String(50))
    capacity = Column(Integer)

    routes = relationship('Route', secondary=transit_airports_routes, back_populates='airports')

class Route(db.Model):
    __tablename__ = 'route'
    routeID = Column(String(10), primary_key= True)
    routeName = Column(String(50))
    departureAirportID = Column(String(10), ForeignKey(Airport.airportID), nullable=False)
    arrivalAirportID = Column(String(10), ForeignKey(Airport.airportID), nullable=False)

    airports = relationship('Airport', secondary=transit_airports_routes, back_populates='routes')

class Flight(db.Model):
    __tablename__ = 'flight'
    flightID = Column(String(15), primary_key= True)
    routeID = Column(String(10), ForeignKey(Route.routeID),nullable=False)
    departureTime = Column(DateTime)
    arrivalTime = Column(DateTime)
    numOf1stClassSeat = Column(Integer)
    numOf2ndClassSeat = Column(Integer)
    flightStatus = Column(Enum('Scheduled','Dalayed', 'Cancelled', 'Completed', name='flight_status'))
    availableSeats = Column(Integer)

    route = relationship(Route)
class SeatClass(db.Model):
    classID = Column(String(10), primary_key=True)
    className = Column(String(50))
    maxCheckedWeight = Column(Integer)
    maxCarryOnWeight= Column(Integer)

class Price(db.Model):
    priceID = Column(String(10),primary_key=True)
    flightID = Column(String(15),ForeignKey(Flight.flightID),nullable=False)
    classID = Column(String(10),ForeignKey(SeatClass.classID),nullable=False)
    price = Column(Float)

    flight = relationship(Flight)
    seat_class = relationship(SeatClass)

class Customer(db.Model):
    __tablename__ = 'customer'
    customerID = Column(String(10), primary_key=True)
    customerName = Column(String(50),nullable=False)
    gender = Column(Enum('Male', 'Female', name= 'customer_gender'))
    birthDate = Column(DateTime)
    idNumber= Column(Integer,nullable=False)
    phoneNumber = Column(Integer,nullable=False)

class Ticket(db.Model):
    __tablename__ = 'ticket'
    ticketID = Column(Integer, primary_key=True,autoincrement=True)
    invoiceID = Column(Integer, ForeignKey('invoice.invoiceID'),nullable=False)
    customerID = Column(String(10), ForeignKey(Customer.customerID),nullable=False)
    flightID = Column(String(15), ForeignKey(Flight.flightID),nullable=False)
    classID = Column(String(10), ForeignKey(SeatClass.classID),nullable=False)
    priceID = Column(String(10), ForeignKey(Price.priceID),nullable=False)
    paid = Column(Boolean, default=False)
    bookingTime = Column(DateTime)

    customer = relationship(Customer)
    flight = relationship(Flight)
    seat_class = relationship(SeatClass)
    price = relationship(Price)


class Invoice(db.Model):
    __tablename__ = 'invoice'
    invoiceID = Column(Integer, primary_key=True, autoincrement=True)
    customerID = Column(String(10), ForeignKey(Customer.customerID),nullable=False)
    paymentAmount = Column(Float,nullable=False)
    paymentStatus = Column(Enum('Pending', 'Paid', 'Cancelled', name='payment_status'))
    paymentMethod = Column(Enum( 'BankTransfer', 'Cash', name='payment_method'))
    paymentTime = Column(DateTime)

    customer = relationship(Customer)
    tickets = relationship(Ticket, backref='invoice')


class Employee(db.Model):
    __tablename__ = 'employee'
    employeeID = Column(String(10),primary_key=True)
    employeeName = Column(String(50))
    birthDate= Column(DateTime)
    employeeRole = Column(Enum('Employee', 'Admin', name='role_enum'))

class Account(db.Model):
    __tablename__ = 'account'
    userName = Column(String(50), primary_key=True)
    password = Column(String(20))
    userRole = Column(Enum('Customer','Employee','Admin', name='userrole_enum'))


