from datetime import datetime

from flask import request, redirect
from sqlalchemy.sql.functions import now
from wtforms.fields.simple import StringField
from wtforms.validators import InputRequired

from ticketbooking.models import Flight, Route, Account, Employee, SystemRule
from ticketbooking import db, app, dao
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user


class FlightView(ModelView):
    column_display_pk = True
    column_searchable_list = ['flightID', 'routeID', 'flightStatus']
    column_filters = ['flightStatus', 'arrivalTime', 'departureTime']
    can_view_details = True
    column_labels = {
        'flightID': 'Mã chuyến bay',
        'routeID': 'Mã tuyến bay',
        'departureTime': 'Thời gian khởi hành',
        'arrivalTime': 'Thời Gian Đến',
        'numOf1stClassSeat': 'Sô ghế hạng 1',
        'numOf2ndClassSeat': 'Số ghế hạng 2',
        'flightStatus': 'Tình trạng chuyến bay',
        'availableSeats': 'Ghế có sẵn'
    }
    def scaffold_form(self):
        form_class = super(FlightView, self).scaffold_form()
        form_class.flightID = StringField('Mã chuyến bay',validators=[InputRequired()])
        form_class.routeID = StringField('Mã tuyến bay',validators=[InputRequired()])
        return form_class

    def is_accessible(self):
        if current_user.is_authenticated and current_user.userRole == 'Admin':
            return True
        return False

class RouteView(ModelView):
    def scaffold_form(self):
        form_class= super(RouteView, self).scaffold_form()
        form_class.flightID = StringField('Mã tuyến bay',validators=[InputRequired()])
        form_class.departureAirportID = StringField('Sân bay đi',validators=[InputRequired()])
        form_class.arrivalAirportID = StringField('Sân bay đến',validators=[InputRequired()])
        return form_class

    def is_accessible(self):
        if current_user.is_authenticated and current_user.userRole == 'Admin':
            return True
        return False

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

    def is_accessible(self):
        if current_user.is_authenticated and current_user.userRole == 'Admin':
            return True
        return False

    column_display_pk = True
    column_searchable_list = ['userName','userRole']
    column_filters = ['userRole']
    can_view_details = True
    column_labels={
        'userName':'Tên người dùng',
        'password':'Mật Khẩu',
        'userRole':'Quyền'
     }

class EmployeeView(ModelView):
    def scaffold_form(self):
        form_class= super(EmployeeView, self).scaffold_form()
        form_class.employeeID = StringField('Mã nhân viên',validators=[InputRequired()])
        return form_class

    def is_accessible(self):
        if current_user.is_authenticated and current_user.userRole == 'Admin':
            return True
        return False

    column_display_pk = True
    column_searchable_list = ['employeeID','employeeName','employeeRole']
    column_filters = ['employeeRole']
    can_view_details = True
    column_labels = {
        'employeeID': 'Mã Nhân Viên',
        'employeeName': 'Tên Nhân Viên',
        'birthDate': 'Ngày sinh',
        'employeeRole': 'Vị trí'
    }
class RuleView(ModelView):

    def is_accessible(self):
        if current_user.is_authenticated and current_user.userRole == 'Admin':
            return True
        return False

    column_searchable_list = ['numAirports', 'minFlightTime', 'maxIntermediatedAirports', 'minStopoverTime',
                              'maxStopoverTime', 'ticketSaleTime_Start', 'ticketBookingTime_Start', 'ticketSaleTime_End'
        , 'ticketBookingTime_End']
    can_view_details = True
    column_labels = {
        'numAirports': 'Số lượng sân bay',
        'minFlightTime': 'Thời gian bay tối thiểu',
        'maxIntermediatedAirports': 'Số lượng sân bay trung gian tối đa',
        'minStopoverTime': 'Thời gian dừng tối thiểu',
        'maxStopoverTime': 'Thời gian dừng tối đa',
        'ticketSaleTime_Start': 'Thời gian bắt đầu bán vé',
        'ticketBookingTime_Start': 'Thời gian bắt đầu đặt vé',
        'ticketSaleTime_End': 'Thời gian kết thúc bán vé',
        'ticketBookingTime_End': 'Thời gian kết thúc đặt vé'
    }

class StatsView(BaseView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.userRole == 'Admin':
            return True
        return False

    @expose('/')
    def index(self, cls=None):
        reportMonth = request.args.get('reportMonth')
        if reportMonth:
            year, month = map(int, reportMonth.split('-'))
        else:
            now = datetime.now()
            year = now.year
            month = now.month

        stats = dao.get_revenue_data_by_month(month=month, year=year)
        total_revenue = sum(s[3] for s in stats)

        return self.render('admin/stats.html', stats=stats, total_revenue=total_revenue)

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/')
    def is_accessible(self):
        if current_user.is_authenticated and current_user.userRole == 'Admin':
            return True
        return False

admin = Admin (app=app, name='Quản Lý Chuyến Bay',template_mode='bootstrap4')
admin.add_view(FlightView(Flight,db.session, name='Chuyến Bay'))
admin.add_view(RouteView(Route,db.session, name='Tuyến Bay'))
admin.add_view(AccountView(Account,db.session, name='Tài Khoản'))
admin.add_view(EmployeeView(Employee,db.session, name ='Nhân Viên'))
admin.add_view(RuleView(SystemRule,db.session, name='Quy định hệ thống'))
admin.add_view(StatsView(name='Thống Kê'))
admin.add_view(LogoutView(name='Đăng Xuất'))
