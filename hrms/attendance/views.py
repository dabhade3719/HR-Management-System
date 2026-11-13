
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.db.models import Count, Q

from .models import Attendance
from .forms import AttendanceForm
from employees.models import Employee


# =========================================================
# ROLE CHECK
# =========================================================

def is_hr_or_admin(user):
    return (
        user.is_authenticated
        and hasattr(user, 'profile')
        and user.profile.role in ['ADMIN', 'HR']
    )


# =========================================================
# ATTENDANCE LIST
# HR / ADMIN ONLY
# =========================================================

@login_required
def attendance_list(request):

    if not is_hr_or_admin(request.user):
        raise PermissionDenied

    records = Attendance.objects.select_related(
        'employee',
        'employee__department'
    ).all()

    search = request.GET.get(
        'search',
        ''
    ).strip()

    selected_date = request.GET.get(
        'date',
        ''
    )

    selected_status = request.GET.get(
        'status',
        ''
    )

    if search:

        records = records.filter(
            Q(employee__employee_id__icontains=search)
            | Q(employee__first_name__icontains=search)
            | Q(employee__last_name__icontains=search)
        )

    if selected_date:
        records = records.filter(
            date=selected_date
        )

    if selected_status:
        records = records.filter(
            status=selected_status
        )

    return render(
        request,
        'attendance/attendance_list.html',
        {
            'records': records,
            'search': search,
            'selected_date': selected_date,
            'selected_status': selected_status,
        }
    )


# =========================================================
# CREATE ATTENDANCE
# HR / ADMIN ONLY
# =========================================================

@login_required
def attendance_create(request):

    if not is_hr_or_admin(request.user):
        raise PermissionDenied

    if request.method == 'POST':

        form = AttendanceForm(
            request.POST
        )

        if form.is_valid():

            try:

                form.save()

                messages.success(
                    request,
                    'Attendance saved successfully.'
                )

                return redirect(
                    'attendance_list'
                )

            except Exception:

                messages.error(
                    request,
                    'Attendance for this employee and date may already exist.'
                )

    else:

        form = AttendanceForm()

    return render(
        request,
        'attendance/attendance_form.html',
        {
            'form': form
        }
    )


# =========================================================
# UPDATE ATTENDANCE
# HR / ADMIN ONLY
# =========================================================

@login_required
def attendance_update(request, id):

    if not is_hr_or_admin(request.user):
        raise PermissionDenied

    record = get_object_or_404(
        Attendance,
        id=id
    )

    if request.method == 'POST':

        form = AttendanceForm(
            request.POST,
            instance=record
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Attendance updated successfully.'
            )

            return redirect(
                'attendance_list'
            )

    else:

        form = AttendanceForm(
            instance=record
        )

    return render(
        request,
        'attendance/attendance_form.html',
        {
            'form': form,
            'record': record
        }
    )


# =========================================================
# DELETE ATTENDANCE
# HR / ADMIN ONLY
# =========================================================

@login_required
def attendance_delete(request, id):

    if not is_hr_or_admin(request.user):
        raise PermissionDenied

    record = get_object_or_404(
        Attendance,
        id=id
    )

    if request.method == 'POST':

        record.delete()

        messages.success(
            request,
            'Attendance deleted successfully.'
        )

        return redirect(
            'attendance_list'
        )

    return render(
        request,
        'attendance/attendance_confirm_delete.html',
        {
            'record': record
        }
    )


# =========================================================
# EMPLOYEE ATTENDANCE
# EMPLOYEE ONLY
# =========================================================

@login_required
def employee_attendance(request):

    if not hasattr(request.user, 'profile'):
        raise PermissionDenied

    if request.user.profile.role != 'EMPLOYEE':
        raise PermissionDenied

    try:

        employee = request.user.employee

    except Exception:

        raise PermissionDenied

    today = timezone.localdate()

    record = Attendance.objects.filter(
        employee=employee,
        date=today
    ).first()

    # -------------------------
    # CHECK IN / CHECK OUT
    # -------------------------

    if request.method == 'POST':

        action = request.POST.get(
            'action'
        )

        # =====================
        # CHECK IN
        # =====================

        if action == 'check_in':

            if record and record.check_in:

                messages.warning(
                    request,
                    'You have already checked in today.'
                )

            else:

                current_time = timezone.localtime().time()

                if record:

                    record.check_in = current_time
                    record.status = 'PRESENT'
                    record.save()

                else:

                    Attendance.objects.create(
                        employee=employee,
                        date=today,
                        check_in=current_time,
                        status='PRESENT'
                    )

                messages.success(
                    request,
                    'Check-in successful!'
                )

        # =====================
        # CHECK OUT
        # =====================

        elif action == 'check_out':

            if not record or not record.check_in:

                messages.error(
                    request,
                    'Please check in before checking out.'
                )

            elif record.check_out:

                messages.warning(
                    request,
                    'You have already checked out today.'
                )

            else:

                record.check_out = timezone.localtime().time()

                record.save()

                messages.success(
                    request,
                    'Check-out successful!'
                )

        else:

            messages.error(
                request,
                'Invalid attendance action.'
            )

        return redirect(
            'employee_attendance'
        )

    return render(
        request,
        'attendance/employee_attendance.html',
        {
            'record': record,
            'today': today,
        }
    )


# =========================================================
# ATTENDANCE REPORT
# HR / ADMIN ONLY
# =========================================================

@login_required
def attendance_report(request):

    if not is_hr_or_admin(request.user):
        raise PermissionDenied

    employees = Employee.objects.all().order_by(
        'first_name'
    )

    selected_employee = request.GET.get(
        'employee',
        ''
    )

    selected_month = request.GET.get(
        'month',
        ''
    )

    records = Attendance.objects.select_related(
        'employee',
        'employee__department'
    ).all()

    # -------------------------
    # EMPLOYEE FILTER
    # -------------------------

    if selected_employee:

        records = records.filter(
            employee_id=selected_employee
        )

    # -------------------------
    # MONTH FILTER
    # -------------------------

    if selected_month:

        try:

            year, month = map(
                int,
                selected_month.split('-')
            )

            if 1 <= month <= 12:

                records = records.filter(
                    date__year=year,
                    date__month=month
                )

            else:

                selected_month = ''

        except (
            ValueError,
            TypeError
        ):

            selected_month = ''

    # -------------------------
    # ATTENDANCE SUMMARY
    # -------------------------

    summary = records.aggregate(

        present=Count(
            'id',
            filter=Q(
                status='PRESENT'
            )
        ),

        absent=Count(
            'id',
            filter=Q(
                status='ABSENT'
            )
        ),

        half_day=Count(
            'id',
            filter=Q(
                status='HALF_DAY'
            )
        ),

        on_leave=Count(
            'id',
            filter=Q(
                status='ON_LEAVE'
            )
        ),
    )

    # -------------------------
    # TOTAL WORKING HOURS
    # -------------------------

    total_working_hours = sum(
        record.working_hours
        for record in records
    )

    return render(
        request,
        'attendance/attendance_report.html',
        {
            'employees': employees,
            'records': records,
            'summary': summary,
            'total_working_hours': round(
                total_working_hours,
                2
            ),
            'selected_employee': selected_employee,
            'selected_month': selected_month,
        }
    )