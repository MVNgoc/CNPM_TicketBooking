from wtforms.fields.simple import StringField
from wtforms.validators import InputRequired

from ticketbooking.models import Flight,Route,Account,Employee
from ticketbooking import db, app
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

class FlightView(ModelView):
    def scaffold_form(self):
        form_class= super(FlightView, self).scaffold_form()
        form_class.flightID = StringField('Mã chuyến bay',validators=[InputRequired()])
        form_class.routeID = StringField('Mã tuyến bay',validators=[InputRequired()])
        return form_class

    column_display_pk = True
    column_searchable_list= ['flightID','routeID','flightStatus']
    column_filters = ['flightStatus','arrivalTime','departureTime']
    can_view_details = True
    column_labels= {
        'flightID': 'Mã chuyến bay',
        'routeID':'Mã tuyến bay',
        'departureTime':'Thời gian khởi hành',
        'arrivalTime': 'Thời Gian Đến',
        'numOf1stClassSeat':'Sô ghế hạng 1',
        'numOf2ndClassSeat':'Số ghế hạng 2',
        'flightStatus':'Tình trạng chuyến bay',
        'availableSeats':'Ghế có sẵn'
    }
class RouteView(ModelView):
    def scaffold_form(self):
        form_class= super(RouteView, self).scaffold_form()
        form_class.flightID = StringField('Mã tuyến bay',validators=[InputRequired()])
        form_class.departureAirportID = StringField('Sân bay đi',validators=[InputRequired()])
        form_class.arrivalAirportID = StringField('Sân bay đến',validators=[InputRequired()])
        return form_class

    column_display_pk = True
    column_filters = ['routeName']
    can_view_details = True
    column_labels={'routeName':'Tên Tuyến Bay',
                   'routeID': 'Mã Tuyến Bay'}

class AccountView(ModelView):
    def scaffold_form(self):
        form_class= super(AccountView, self).scaffold_form()
        form_class.userName = StringField('Tên người dùng',validators=[InputRequired()])
        return form_class
    column_display_pk = True
    column_searchable_list = ['userName','userRole']
    column_filters = ['userRole']
    can_view_details = True
    column_labels={
        'userName':'Tên Người dùng',
        'password':'Mật Khẩu',
        'userRole':'Người Dùng'
     }

    def is_accessible(self):
        return current_user.is_authenticated
class EmployeeView(ModelView):
    def scaffold_form(self):
        form_class= super(EmployeeView, self).scaffold_form()
        form_class.employeeID = StringField('Mã nhân viên',validators=[InputRequired()])
        return form_class
    column_display_pk = True
    column_searchable_list = ['employeeID','employeeName','employeeRole']
    column_filters = ['employeeRole']
    can_view_details = True
    column_labels = {
        'employeeID': 'Mã Nhân Viên',
        'employeeName': 'Tên Nhân Viên',
        'birthDate': 'Ngày sinh',
        'employeeRole': 'Chức năng'
    }


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')

admin = Admin (app=app, name='Quản Lý Chuyến Bay',template_mode='bootstrap4')
admin.add_view(FlightView(Flight,db.session, name='Chuyến Bay'))
admin.add_view(RouteView(Route,db.session, name='Tuyến Bay'))
admin.add_view(AccountView(Account,db.session, name ='Tài Khoản'))
admin.add_view(EmployeeView(Employee,db.session, name = 'Nhân Viên'))
admin.add_view(StatsView(name='Thống Kê'))