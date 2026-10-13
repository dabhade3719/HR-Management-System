
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from notifications.models import Notification
from django.contrib.auth.models import User


from .models import LeaveRequest


# =========================================================
# APPLY LEAVE
# Employee can apply for leave
# =========================================================

@login_required
def apply_leave(request):

    if request.method == 'POST':

        leave_type = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason', '').strip()

        # Check empty fields
        if not all([
            leave_type,
            start_date,
            end_date,
            reason
        ]):
            messages.error(
                request,
                'Please fill all fields.'
            )
            return redirect('apply_leave')

        # Check leave type
        if leave_type not in dict(
            LeaveRequest.LEAVE_TYPE_CHOICES
        ):
            messages.error(
                request,
                'Invalid leave type.'
            )
            return redirect('apply_leave')

        # Convert dates
        try:

            start = timezone.datetime.strptime(
                start_date,
                '%Y-%m-%d'
            ).date()

            end = timezone.datetime.strptime(
                end_date,
                '%Y-%m-%d'
            ).date()

        except ValueError:

            messages.error(
                request,
                'Invalid date.'
            )
            return redirect('apply_leave')

        # Past date check
        if start < timezone.localdate():

            messages.error(
                request,
                'Past dates are not allowed.'
            )
            return redirect('apply_leave')

        # End date check
        if end < start:

            messages.error(
                request,
                'End date cannot be before start date.'
            )
            return redirect('apply_leave')

        # Create leave request
        LeaveRequest.objects.create(
            employee=request.user,
            leave_type=leave_type,
            start_date=start,
            end_date=end,
            reason=reason
        )

        # Notify HR and Admin
        hr_admin_users = User.objects.filter(
            profile__role__in=['HR', 'ADMIN']
            )
        for user in hr_admin_users:
            Notification.objects.create(
                user=user,
                title="New Leave Request",
                message=f"{request.user.username} has submitted a new leave request.",
                notification_type="LEAVE"
                )

        messages.success(
            request,
            'Leave request submitted successfully!'
        )

        return redirect('my_leaves')

    return render(
        request,
        'leaves/apply_leave.html'
    )


# =========================================================
# MY LEAVES
# Employee can see ONLY their own leaves
# =========================================================

@login_required
def my_leaves(request):

    leaves = LeaveRequest.objects.filter(
        employee=request.user
    ).order_by('-applied_on')

    return render(
        request,
        'leaves/my_leaves.html',
        {
            'leaves': leaves
        }
    )


# =========================================================
# MANAGE LEAVES
# Only ADMIN and HR
# =========================================================

@login_required
def manage_leaves(request):

    if not hasattr(request.user, 'profile'):
        raise PermissionDenied

    if request.user.profile.role not in [
        'ADMIN',
        'HR'
    ]:
        raise PermissionDenied

    leaves = LeaveRequest.objects.select_related(
        'employee',
        'reviewed_by'
    ).all().order_by('-applied_on')

    return render(
        request,
        'leaves/manage_leaves.html',
        {
            'leaves': leaves
        }
    )


# =========================================================
# REVIEW LEAVE
# Only ADMIN and HR
# =========================================================

@login_required
@require_POST
def review_leave(request, id):

    if not hasattr(request.user, 'profile'):
        raise PermissionDenied

    if request.user.profile.role not in [
        'ADMIN',
        'HR'
    ]:
        raise PermissionDenied

    leave = get_object_or_404(
        LeaveRequest,
        id=id
    )

    action = request.POST.get('action')

    comment = request.POST.get(
        'review_comment',
        ''
    ).strip()

    # Already reviewed
    if leave.status != 'PENDING':

        messages.warning(
            request,
            'This leave request has already been reviewed.'
        )

        return redirect('manage_leaves')

    # Approve
    if action == 'approve':

        leave.status = 'APPROVED'

    # Reject
    elif action == 'reject':

        leave.status = 'REJECTED'

    else:

        messages.error(
            request,
            'Invalid action.'
        )

        return redirect('manage_leaves')

    # Save reviewer information
    leave.reviewed_by = request.user

    leave.review_comment = comment

    leave.save()
    # Notify employee about leave decision
    Notification.objects.create(
        user=leave.employee,
        title="Leave Request Update",
        message=f"Your leave request has been {leave.status.lower()}.",
        notification_type="LEAVE"
        )

    messages.success(
        request,
        f'Leave request {leave.status.lower()} successfully.'
    )

    return redirect('manage_leaves')