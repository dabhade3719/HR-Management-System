from datetime import date

from .models import Employee


def generate_employee_id():
    """Next free ID like EMP0001, EMP0002 ..."""
    last = Employee.objects.order_by('-id').first()
    number = (last.id + 1) if last else 1

    while Employee.objects.filter(employee_id=f"EMP{number:04d}").exists():
        number += 1

    return f"EMP{number:04d}"


def get_or_create_employee(user, first_name='', last_name='', phone=''):
    """
    Return the Employee linked to this user. If none exists yet
    (e.g. the user just registered), create one with safe defaults.
    HR can complete department / designation / salary later.
    """
    employee = Employee.objects.filter(user=user).first()

    if employee:
        return employee

    return Employee.objects.create(
        user=user,
        employee_id=generate_employee_id(),
        first_name=first_name or user.first_name or user.username,
        last_name=last_name or user.last_name or '',
        email=user.email,
        phone=phone,
        designation='Not Assigned',
        joining_date=date.today(),
        gender='OTHER',
        salary=0,
        employment_status='ACTIVE',
    )
