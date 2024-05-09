from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, Float, DateTime, Enum, Time, LargeBinary
from sqlalchemy.orm import relationship
from ticketbooking import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin

transit_airports_routes = Table(
    'transit_airports_routes',
    db.metadata,
    Column('airport_id', String(10), ForeignKey('airport.airportID'), primary_key=True),
    Column('route_id', String(10), ForeignKey('route.routeID'), primary_key=True),
    extend_existing=True
)


class Airport(db.Model):
    __tablename__ = 'airport'
    airportID = Column(String(10), primary_key=True)
    airportName = Column(String(100), nullable=False)
    locationCity = Column(String(50))
    locationCountry = Column(String(50))
    capacity = Column(Integer)

    routes = relationship('Route', secondary=transit_airports_routes, back_populates='airports')
    __table_args__ = {'extend_existing': True}

class Route(db.Model):
    __tablename__ = 'route'
    routeID = Column(String(10), primary_key=True)
    routeName = Column(String(50))
    departureAirportID = Column(String(10), ForeignKey(Airport.airportID), nullable=False)
    arrivalAirportID = Column(String(10), ForeignKey(Airport.airportID), nullable=False)

    airports = relationship('Airport', secondary=transit_airports_routes, back_populates='routes')
    __table_args__ = {'extend_existing': True}

class Flight(db.Model):
    __tablename__ = 'flight'
    flightID = Column(String(15), primary_key=True)
    routeID = Column(String(10), ForeignKey(Route.routeID), nullable=False)
    departureTime = Column(DateTime)
    arrivalTime = Column(DateTime)
    numOf1stClassSeat = Column(Integer)
    numOf2ndClassSeat = Column(Integer)
    flightStatus = Column(Enum('Scheduled', 'Delayed', 'Cancelled', 'Completed', name='flight_status'))
    availableSeats = Column(Integer)

    route = relationship(Route)
    __table_args__ = {'extend_existing': True}

class SeatClass(db.Model):
    __tablename__ = 'seat_class'
    classID = Column(String(10), primary_key=True)
    className = Column(String(50))
    maxCheckedWeight = Column(Integer)
    maxCarryOnWeight = Column(Integer)
    __table_args__ = {'extend_existing': True}

class Price(db.Model):
    __tablename__ = 'price'
    priceID = Column(String(10), primary_key=True)
    flightID = Column(String(15), ForeignKey(Flight.flightID), nullable=False)
    classID = Column(String(10), ForeignKey(SeatClass.classID), nullable=False)
    price = Column(Float)

    flight = relationship(Flight)
    seat_class = relationship(SeatClass)
    __table_args__ = {'extend_existing': True}

class Customer(db.Model):
    __tablename__ = 'customer'
    customerID = Column(String(10), primary_key=True)
    customerName = Column(String(50), nullable=False)
    gender = Column(Enum('Male', 'Female', name='customer_gender'))
    birthDate = Column(DateTime)
    idNumber = Column(Integer, nullable=False)
    phoneNumber = Column(Integer, nullable=False)
    __table_args__ = {'extend_existing': True}

class Ticket(db.Model):
    __tablename__ = 'ticket'
    ticketID = Column(Integer, primary_key=True, autoincrement=True)
    invoiceID = Column(Integer, ForeignKey('invoice.invoiceID'), nullable=False)
    customerID = Column(String(10), ForeignKey(Customer.customerID), nullable=False)
    accountID = Column(Integer, ForeignKey('account.id'), nullable=False)
    flightID = Column(String(15), ForeignKey(Flight.flightID), nullable=False)
    classID = Column(String(10), ForeignKey(SeatClass.classID), nullable=False)
    priceID = Column(String(10), ForeignKey(Price.priceID), nullable=False)


    customer = relationship(Customer)
    flight = relationship(Flight)
    seat_class = relationship(SeatClass)
    price = relationship(Price)
    account = relationship("Account")
    __table_args__ = {'extend_existing': True}

class Employee(db.Model):
    __tablename__ = 'employee'
    employeeID = Column(String(10), primary_key=True)
    employeeName = Column(String(50))
    birthDate = Column(DateTime)
    employeeRole = Column(Enum('Employee', 'Admin', name='role_enum'))
    __table_args__ = {'extend_existing': True}

class Account(db.Model, UserMixin):
    __tablename__ = 'account'
    id = Column(Integer, autoincrement=True, primary_key=True)
    userName = Column(String(50), unique=True)
    password = Column(String(1000), nullable=True)
    userRole = Column(Enum('Customer', 'Employee', 'Admin', name='userrole_enum'))
    __table_args__ = {'extend_existing': True}
    def __str__(self):
        return self.userName

class Invoice(db.Model):
    __tablename__ = 'invoice'
    invoiceID = Column(Integer, primary_key=True, autoincrement=True)
    accountID = Column(Integer,ForeignKey(Account.id), nullable=False)
    paymentAmount = Column(Float, nullable=False)
    paymentStatus = Column(Enum('Pending', 'Paid', 'Cancelled', name='payment_status'))
    paymentMethod = Column(Enum('BankTransfer', 'Cash', name='payment_method'))
    transferImage = Column(LargeBinary)
    paymentTime = Column(DateTime)

    tickets = relationship(Ticket, backref='invoice')
    account = relationship(Account)
    __table_args__ = {'extend_existing': True}

class SystemRule(db.Model):
    __tablename__ = 'system_rule'
    id = Column(Integer, primary_key=True, autoincrement=True)
    numAirports = Column(Integer, nullable=False)  # Số lượng sân bay
    minFlightTime = Column(Float, nullable=False)  # Thời gian bay tối thiểu
    maxIntermediatedAirports = Column(Integer, nullable=False)  # Số sân bay trung gian tối đa
    minStopoverTime = Column(Float, nullable=False)  # Thời gian dừng tối thiểu tại các sân bay trung gian
    maxStopoverTime = Column(Float, nullable=False)  # Thời gian dừng tối đa tại các sân bay trung gian
    ticketSaleTime_Start= Column(Time, nullable=False)  # Thời gian bắt đầu bán vé
    ticketBookingTime_Start= Column(Time, nullable=False)  # Thời gian bắt đầu đặt vé
    ticketSaleTime_End = Column(Time, nullable=False)  # Thời gian kết thúc bán vé
    ticketBookingTime_End= Column(Time, nullable=False)  # Thời gian kết thúc đặt vé
    __table_args__ = {'extend_existing': True}

    def __str__(self):
        return self.userName
