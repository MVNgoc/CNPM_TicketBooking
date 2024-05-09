from ticketbooking import db, app
from models import Account, Airport, Route, Flight, SeatClass, Price, Customer, Invoice, Ticket, Employee, SystemRule
from datetime import datetime, time
import hashlib


def create_database():
    db.create_all()


def add_sample_data():
    airport1 = Airport(airportID='TSN', airportName='Tan Son Nhat International Airport', locationCity='Hồ Chí Minh')
    airport2 = Airport(airportID='PQC', airportName='Phu Quoc International Airport', locationCity='Phú Quốc')
    airport3 = Airport(airportID='HAN', airportName='Noi Bai International Airport', locationCity='Hà Nội')
    airport4 = Airport(airportID='DAD', airportName='Da Nang International Airport', locationCity='Đà Nẵng')
    airport5 = Airport(airportID='VDO', airportName='Van Don International Airport', locationCity='Quảng Ninh')
    airport6 = Airport(airportID='HUI', airportName='Phu Bai International Airport', locationCity='Huế')

    route1 = Route(routeID='R001', routeName='HCMC-PQC', departureAirportID='TSN', arrivalAirportID='PQC')
    route2 = Route(routeID='R002', routeName='HCMC-HNC', departureAirportID='TSN', arrivalAirportID='HAN')
    route3 = Route(routeID='R003', routeName='HCMC-DNC', departureAirportID='TSN', arrivalAirportID='DAD')
    route4 = Route(routeID='R004', routeName='PQC-HCMC', departureAirportID='PQC', arrivalAirportID='TSN')
    route5 = Route(routeID='R005', routeName='HCMC-HC', departureAirportID='TSN', arrivalAirportID='HUI')
    route6 = Route(routeID='R006', routeName='HC-HCMC', departureAirportID='HUI', arrivalAirportID='TSN')

    flight1 = Flight(flightID='F001', routeID='R001',
                     departureTime=datetime.strptime('2024-5-20 08:00:00', '%Y-%m-%d %H:%M:%S'),
                     arrivalTime=datetime.strptime('2024-5-20 11:00:00', '%Y-%m-%d %H:%M:%S'), numOf1stClassSeat=100,
                     numOf2ndClassSeat=200, flightStatus='Scheduled', availableSeats=300)
    flight2 = Flight(flightID='F002', routeID='R001',
                     departureTime=datetime.strptime('2024-5-20 08:00:00', '%Y-%m-%d %H:%M:%S'),
                     arrivalTime=datetime.strptime('2024-5-20 11:00:00', '%Y-%m-%d %H:%M:%S'), numOf1stClassSeat=100,
                     numOf2ndClassSeat=200, flightStatus='Scheduled', availableSeats=300)
    flight3 = Flight(flightID='F003', routeID='R001',
                     departureTime=datetime.strptime('2024-5-21 08:00:00', '%Y-%m-%d %H:%M:%S'),
                     arrivalTime=datetime.strptime('2024-5-21 11:00:00', '%Y-%m-%d %H:%M:%S'), numOf1stClassSeat=100,
                     numOf2ndClassSeat=200, flightStatus='Scheduled', availableSeats=300)
    flight4 = Flight(flightID='F004', routeID='R002',
                     departureTime=datetime.strptime('2024-5-20 08:00:00', '%Y-%m-%d %H:%M:%S'),
                     arrivalTime=datetime.strptime('2024-5-20 11:00:00', '%Y-%m-%d %H:%M:%S'), numOf1stClassSeat=100,
                     numOf2ndClassSeat=200, flightStatus='Scheduled', availableSeats=300)
    flight5 = Flight(flightID='F005', routeID='R002',
                     departureTime=datetime.strptime('2024-5-21 08:00:00', '%Y-%m-%d %H:%M:%S'),
                     arrivalTime=datetime.strptime('2024-5-21 11:00:00', '%Y-%m-%d %H:%M:%S'), numOf1stClassSeat=100,
                     numOf2ndClassSeat=200, flightStatus='Scheduled', availableSeats=300)
    flight6 = Flight(flightID='F006', routeID='R002',
                     departureTime=datetime.strptime('2024-5-21 08:00:00', '%Y-%m-%d %H:%M:%S'),
                     arrivalTime=datetime.strptime('2024-5-21 11:00:00', '%Y-%m-%d %H:%M:%S'), numOf1stClassSeat=100,
                     numOf2ndClassSeat=200, flightStatus='Scheduled', availableSeats=300)

    seat_class1 = SeatClass(classID='SC001', className='First Class', maxCheckedWeight=32, maxCarryOnWeight=10)
    seat_class2 = SeatClass(classID='SC002', className='Economy Class', maxCheckedWeight=20, maxCarryOnWeight=7)

    price1 = Price(priceID='P001', flightID='F001', classID='SC001', price=100.0)
    price2 = Price(priceID='P002', flightID='F001', classID='SC002', price=50.0)

    customer1 = Customer(customerID='C001', customerName='John Doe', gender='Male',
                         birthDate=datetime.strptime('1997-4-6 00:00:00', '%Y-%m-%d %H:%M:%S'), idNumber=123456789,
                         phoneNumber=987654321)
    customer2 = Customer(customerID='C002', customerName='Abc', gender='Female',
                         birthDate=datetime.strptime('1997-4-6 00:00:00', '%Y-%m-%d %H:%M:%S'), idNumber=123456789,
                         phoneNumber=987654321)

    invoice1 = Invoice(invoiceID=1, accountID = '1', paymentAmount=100.0, paymentStatus='Paid', paymentMethod='Cash',
                       paymentTime=datetime.strptime('2024-4-18 16:30:00', '%Y-%m-%d %H:%M:%S'))
    invoice2 = Invoice(invoiceID=2, accountID = '1', paymentAmount=100.0, paymentStatus='Paid', paymentMethod='Cash',
                       paymentTime=datetime.strptime('2024-4-19 16:30:00', '%Y-%m-%d %H:%M:%S'))
    invoice3 = Invoice(invoiceID=3, accountID = '1', paymentAmount=100.0, paymentStatus='Paid', paymentMethod='Cash',
                       paymentTime=datetime.strptime('2024-4-20 16:30:00', '%Y-%m-%d %H:%M:%S'))
    invoice4 = Invoice(invoiceID=4, accountID = '2', paymentAmount=100.0, paymentStatus='Paid', paymentMethod='Cash',
                       paymentTime=datetime.strptime('2024-4-20 16:30:00', '%Y-%m-%d %H:%M:%S'))
    invoice5 = Invoice(invoiceID=5, accountID = '1', paymentAmount=100.0, paymentStatus='Paid', paymentMethod='Cash',
                       paymentTime=datetime.strptime('2024-4-22 16:30:00', '%Y-%m-%d %H:%M:%S'))
    invoice6 = Invoice(invoiceID=6, accountID = '1', paymentAmount=100.0, paymentStatus='Paid', paymentMethod='Cash',
                       paymentTime=datetime.strptime('2024-4-23 16:30:00', '%Y-%m-%d %H:%M:%S'))

    ticket1 = Ticket(invoiceID=1, customerID='C001', accountID='1', flightID='F001', classID='SC001', priceID='P001')

    employee1 = Employee(employeeID='E001', employeeName='Jane Smith',
                         birthDate=datetime.strptime('1996-7-17 00:00:00', '%Y-%m-%d %H:%M:%S'), employeeRole='Admin')
    employee2 = Employee(employeeID='E002', employeeName='Jesscica Huynh',
                         birthDate=datetime.strptime('2000-1-1 00:00:00', '%Y-%m-%d %H:%M:%S'), employeeRole='Employee')


    account1 = Account(id=1, userName='JohnDoe64', password=str(hashlib.md5("johndoe64@@".encode('utf-8')).hexdigest()),userRole='Customer')
    account2 = Account(id=2, userName='E001', password=str(hashlib.md5("admine001.,".encode('utf-8')).hexdigest()),userRole='Admin')
    account3 = Account(id=3, userName='E002', password=str(hashlib.md5("employeeE002..".encode('utf-8')).hexdigest()),userRole='Employee')

    system_rule = SystemRule(numAirports=2, minFlightTime=3.5, maxIntermediatedAirports=1, minStopoverTime=1.5,
                             maxStopoverTime=4.0, ticketSaleTime_Start=time(hour=8), ticketBookingTime_Start=time(
            hour=8), ticketSaleTime_End=time(hour=17),  ticketBookingTime_End=time(
            hour=23) )  # Thời gian bắt đầu bán vé từ 8 giờ sáng   # Thời gian bắt đầu đặt vé từ 8 giờ sáng

    db.session.add_all(
        [airport1, airport2, airport3, airport4, airport5, airport6,
         route1, route2, route3, route4, route5, route6,
         flight1, flight2, flight3, flight4, flight5, flight6,
         seat_class1, seat_class2,
         price1, price2,
         customer1, customer2,
         invoice1, invoice2, invoice3, invoice4, invoice5, invoice6,
         ticket1,
         employee1, employee2,
         system_rule,
         account1, account2, account3])
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        create_database()
        add_sample_data()
