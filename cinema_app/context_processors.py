import datetime
from employee_app.mixins import is_employee

def cinema_info(request):
    return {
        'current_year': datetime.date.today().year,
    }
  

def employee_access(request):
    return {'is_employee': is_employee(request.user)}