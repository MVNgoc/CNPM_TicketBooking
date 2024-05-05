from ticketbooking import db,app
from models import Account, Airport, Route, Flight, SeatClass, Price, Customer, Invoice, Ticket, Employee
from datetime import datetime
import hashlib


def create_database():
    db.create_all()


def add_sample_data():
    airport1 = Airport(airportID='TSN', airportName='Tan Son Nhat International Airport')
    airport2 = Airport(airportID='PQC', airportName='Phu Quoc International Airport')

    route1 = Route(routeID='R001', routeName='HCMC-PQC', departureAirportID='TSN', arrivalAirportID='PQC')

    flight1 = Flight(flightID='F001', routeID='R001', departureTime=datetime.strptime('2024-4-20 08:00:00','%Y-%m-%d %H:%M:%S'), arrivalTime=datetime.strptime('2024-4-20 11:00:00','%Y-%m-%d %H:%M:%S'), numOf1stClassSeat=100, numOf2ndClassSeat=200, flightStatus='Scheduled', availableSeats=300)

    seat_class1 = SeatClass(classID='SC001', className='First Class', maxCheckedWeight=32, maxCarryOnWeight=10)
    seat_class2 = SeatClass(classID='SC002', className='Economy Class', maxCheckedWeight=20, maxCarryOnWeight=7)

    price1 = Price(priceID='P001', flightID='F001', classID='SC001', price=100.0)
    price2 = Price(priceID='P002', flightID='F001', classID='SC002', price=50.0)

    customer1 = Customer(customerID='C001', customerName='John Doe', gender='Male', birthDate=datetime.strptime('1997-4-6 00:00:00','%Y-%m-%d %H:%M:%S'), idNumber=123456789, phoneNumber=987654321)

    invoice1 = Invoice(invoiceID=1, customerID='C001', paymentAmount=100.0, paymentStatus='Paid', paymentMethod='Cash', paymentTime=datetime.strptime('2024-4-18 16:30:00','%Y-%m-%d %H:%M:%S'))

    ticket1 = Ticket(invoiceID=1, customerID='C001', flightID='F001', classID='SC001', priceID='P001', bookingTime=datetime.strptime('2024-4-18 16:30:00','%Y-%m-%d %H:%M:%S'), paid=True)

    employee1 = Employee(employeeID='E001', employeeName='Jane Smith', birthDate=datetime.strptime('1996-7-17 00:00:00','%Y-%m-%d %H:%M:%S'), employeeRole='Admin')
    employee2 = Employee(employeeID='E002', employeeName='Jesscica Huynh', birthDate=datetime.strptime('2000-1-1 00:00:00','%Y-%m-%d %H:%M:%S'), employeeRole='Employee')

    account1 = Account(id=1, userName='JohnDoe64', password=str(hashlib.md5("johndoe64@@".encode('utf-8')).hexdigest()), userRole='Customer')
    account2 = Account(id=2, userName='E001', password=str(hashlib.md5("admine001.,".encode('utf-8')).hexdigest()), userRole='Admin')
    account3 = Account(id=3, userName='E002', password=str(hashlib.md5("employeeE002..".encode('utf-8')).hexdigest()), userRole='Employee')

    db.session.add_all([account1, account2, account3])
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        create_database()
        add_sample_data()