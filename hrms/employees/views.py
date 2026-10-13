from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from accounts.models import Profile
from departments.models import Department

from .models import Employee
from .forms import EmployeeForm


# =========================
# EMPLOYEE CREATE
# =========================

@login_required
def employee_create(request):

    if not hasattr(request.user, 'profile'):
        raise PermissionDenied

    if request.user.profile.role not in ['ADMIN', 'HR']:
        raise PermissionDenied

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)

        if form.is_valid():
            username = form.cleaned_data['username']

            user = User.objects.get(username=username)

            # Prevent linking the same user to multiple employees.
            if Employee.objects.filter(user=user).exists():
                form.add_error(
                    'username',
                    'This user already has an employee record.'
                )
            else:
                employee = form.save(commit=False)
                employee.user = user
                employee.save()

                # Ensure the existing user has an Employee role.
                Profile.objects.update_or_create(
                    user=user,
                    defaults={'role': 'EMPLOYEE'}
                )

                messages.success(
                    request,
                    'Employee record created successfully.'
                )

                return redirect('employee_list')

    else:
        form = EmployeeForm()

    return render(
        request,
        'employees/employee_form.html',
        {'form': form}
    )

# =========================
# EMPLOYEE LIST
# =========================

@login_required
def employee_list(request):

    if not hasattr(request.user, 'profile'):
        raise PermissionDenied

    if request.user.profile.role not in ['ADMIN', 'HR']:
        raise PermissionDenied

    employees = Employee.objects.select_related(
        'department',
        'user'
    ).all()

    search = request.GET.get(
        'search',
        ''
    ).strip()

    department = request.GET.get(
        'department',
        ''
    )

    status = request.GET.get(
        'status',
        ''
    )

    if search:

        employees = employees.filter(
            employee_id__icontains=search
        ) | employees.filter(
            first_name__icontains=search
        ) | employees.filter(
            last_name__icontains=search
        ) | employees.filter(
            email__icontains=search
        )

    if department:
        employees = employees.filter(
            department_id=department
        )

    if status:
        employees = employees.filter(
            employment_status=status
        )

    departments = Department.objects.filter(
        is_active=True
    )

    return render(
        request,
        'employees/employee_list.html',
        {
            'employees': employees,
            'departments': departments,
            'search': search,
            'selected_department': department,
            'selected_status': status,
        }
    )


# =========================
# EMPLOYEE UPDATE
# =========================

@login_required
def employee_update(request, id):

    if not hasattr(request.user, 'profile'):
        raise PermissionDenied

    if request.user.profile.role not in ['ADMIN', 'HR']:
        raise PermissionDenied

    employee = get_object_or_404(
        Employee,
        id=id
    )

    if request.method == 'POST':

        form = EmployeeForm(
            request.POST,
            request.FILES,
            instance=employee
        )

        if form.is_valid():

            employee = form.save()

            employee.user.email = employee.email
            employee.user.save()

            messages.success(
                request,
                "Employee updated successfully."
            )

            return redirect('employee_list')

    else:

        form = EmployeeForm(
            instance=employee
        )

    return render(
        request,
        'employees/employee_form.html',
        {
            'form': form,
            'employee': employee
        }
    )


# =========================
# EMPLOYEE DELETE
# =========================

@login_required
def employee_delete(request, id):

    if not hasattr(request.user, 'profile'):
        raise PermissionDenied

    if request.user.profile.role not in ['ADMIN', 'HR']:
        raise PermissionDenied

    employee = get_object_or_404(
        Employee,
        id=id
    )

    if request.method == 'POST':

        employee.user.delete()

        messages.success(
            request,
            "Employee deleted successfully."
        )

        return redirect('employee_list')

    return render(
        request,
        'employees/employee_confirm_delete.html',
        {
            'employee': employee
        }
    )


# =========================
# EMPLOYEE DETAIL
# =========================

@login_required
def employee_detail(request, id):

    if not hasattr(request.user, 'profile'):
        raise PermissionDenied

    if request.user.profile.role not in ['ADMIN', 'HR']:
        raise PermissionDenied

    employee = get_object_or_404(
        Employee.objects.select_related(
            'department',
            'user'
        ),
        id=id
    )

    return render(
        request,
        'employees/employee_detail.html',
        {
            'employee': employee
        }
    )


# =========================
# EMPLOYEE PROFILE
# =========================

@login_required
def employee_profile(request):

    if not hasattr(request.user, 'profile'):
        raise PermissionDenied

    employee = Employee.objects.filter(
        user=request.user
    ).first()

    if not employee:
        raise PermissionDenied

    if request.method == 'POST':

        employee.email = request.POST.get(
            'email',
            ''
        ).strip()

        employee.phone = request.POST.get(
            'phone',
            ''
        ).strip()

        employee.address = request.POST.get(
            'address',
            ''
        ).strip()

        if request.FILES.get('profile_photo'):

            employee.profile_photo = request.FILES.get(
                'profile_photo'
            )

        employee.save()

        request.user.email = employee.email
        request.user.save()

        messages.success(
            request,
            "Profile updated successfully."
        )

        return redirect(
            'employee_profile'
        )

    return render(
        request,
        'employees/employee_profile.html',
        {
            'employee': employee
        }
    )