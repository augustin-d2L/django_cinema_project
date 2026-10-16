import datetime
from employee_app.mixins import EMPLOYEE_GROUPS

def cinema_info(request):
    return {
        'current_year': datetime.date.today().year,
    }

def employee_access(request):
    user = request.user
    return {
        'is_employee': user.is_authenticated and (
            user.is_superuser or user.groups.filter(name__in=EMPLOYEE_GROUPS).exists()
        ),
    }