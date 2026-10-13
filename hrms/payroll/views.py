
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from notifications.models import Notification

from .models import Payroll


def is_hr_or_admin(user):
    return (
        user.is_authenticated
        and hasattr(user, 'profile')
        and user.profile.role in ['ADMIN', 'HR']
    )


@login_required
def payroll_list(request):

    if not is_hr_or_admin(request.user):
        raise PermissionDenied

    payrolls = Payroll.objects.select_related(
        'employee'
    ).all().order_by('-year', '-month')

    return render(
        request,
        'payroll/payroll_list.html',
        {
            'payrolls': payrolls
        }
    )


@login_required
def my_payroll(request):

    if not hasattr(request.user, 'profile'):
        raise PermissionDenied

    if request.user.profile.role != 'EMPLOYEE':
        raise PermissionDenied

    payrolls = Payroll.objects.filter(
        employee=request.user
    ).order_by('-year', '-month')

    return render(
        request,
        'payroll/my_payroll.html',
        {
            'payrolls': payrolls
        }
    )