
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.db.models import Q

from notifications.models import Notification
from .models import JobOpening, JobApplication


def is_hr_or_admin(user):
    return (
        user.is_authenticated
        and hasattr(user, 'profile')
        and user.profile.role in ['ADMIN', 'HR']
    )


def require_hr_admin(user):
    if not is_hr_or_admin(user):
        raise PermissionDenied


# =========================
# RECRUITMENT DASHBOARD
# =========================
@login_required
def recruitment_dashboard(request):
    require_hr_admin(request.user)

    jobs = JobOpening.objects.all().order_by('-posted_on')
    applications = JobApplication.objects.select_related(
        'job'
    ).all().order_by('-applied_on')

    context = {
        'jobs': jobs,
        'applications': applications,
        'total_jobs': jobs.count(),
        'active_jobs': jobs.filter(is_active=True).count(),
        'inactive_jobs': jobs.filter(is_active=False).count(),
        'total_applications': applications.count(),
        'pending_applications': applications.filter(
            status='APPLIED'
        ).count(),
    }

    return render(
        request,
        'requirement/requirement_dashboard.html',
        context
    )


# =========================
# CREATE JOB
# =========================
@login_required
def create_job(request):
    require_hr_admin(request.user)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        department = request.POST.get('department', '').strip()
        location = request.POST.get('location', '').strip()
        job_type = request.POST.get('job_type', 'FULL_TIME')
        description = request.POST.get('description', '').strip()
        requirements = request.POST.get('requirements', '').strip()
        salary_range = request.POST.get('salary_range', '').strip()
        vacancies = request.POST.get('vacancies', '1').strip()

        if not all([
            title, department, location,
            description, requirements, vacancies
        ]):
            messages.error(request, 'Please fill all required fields.')
            return render(
                request,
                'requirement/create_job.html',
                {'job_types': JobOpening.JOB_TYPE_CHOICES}
            )

        try:
            vacancies = int(vacancies)
            if vacancies < 1:
                raise ValueError
        except ValueError:
            messages.error(request, 'Vacancies must be at least 1.')
            return render(
                request,
                'requirement/create_job.html',
                {'job_types': JobOpening.JOB_TYPE_CHOICES}
            )

        valid_job_types = [
            choice[0] for choice in JobOpening.JOB_TYPE_CHOICES
        ]

        if job_type not in valid_job_types:
            messages.error(request, 'Please select a valid job type.')
            return redirect('create_job')

        job = JobOpening.objects.create(
            title=title,
            department=department,
            location=location,
            job_type=job_type,
            description=description,
            requirements=requirements,
            salary_range=salary_range,
            vacancies=vacancies,
            is_active=True
        )

        employees = User.objects.filter(profile__role='EMPLOYEE')

        Notification.objects.bulk_create([
            Notification(
                user=employee,
                title='New Job Opportunity',
                message=f'New job posted: {job.title}',
                notification_type='JOB'
            )
            for employee in employees
        ])

        messages.success(request, 'Job created successfully!')
        return redirect('recruitment_dashboard')

    return render(
        request,
        'requirement/create_job.html',
        {'job_types': JobOpening.JOB_TYPE_CHOICES}
    )


# =========================
# EDIT JOB
# =========================
@login_required
def edit_job(request, job_id):
    require_hr_admin(request.user)

    job = get_object_or_404(JobOpening, id=job_id)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        department = request.POST.get('department', '').strip()
        location = request.POST.get('location', '').strip()
        job_type = request.POST.get('job_type', '')
        description = request.POST.get('description', '').strip()
        requirements = request.POST.get('requirements', '').strip()
        salary_range = request.POST.get('salary_range', '').strip()
        vacancies = request.POST.get('vacancies', '').strip()

        if not all([
            title, department, location,
            job_type, description, requirements, vacancies
        ]):
            messages.error(request, 'Please fill all required fields.')
        else:
            try:
                vacancies = int(vacancies)
                if vacancies < 1:
                    raise ValueError

                valid_job_types = [
                    choice[0]
                    for choice in JobOpening.JOB_TYPE_CHOICES
                ]

                if job_type not in valid_job_types:
                    raise ValueError

            except ValueError:
                messages.error(
                    request,
                    'Please enter valid job type and vacancies (minimum 1).'
                )
            else:
                job.title = title
                job.department = department
                job.location = location
                job.job_type = job_type
                job.description = description
                job.requirements = requirements
                job.salary_range = salary_range
                job.vacancies = vacancies
                job.save()

                messages.success(request, 'Job updated successfully!')
                return redirect('recruitment_dashboard')

    return render(
        request,
        'requirement/edit_job.html',
        {
            'job': job,
            'job_types': JobOpening.JOB_TYPE_CHOICES,
        }
    )


# =========================
# ACTIVATE / DEACTIVATE JOB
# =========================
@login_required
def toggle_job_status(request, job_id):
    require_hr_admin(request.user)

    if request.method != 'POST':
        return redirect('recruitment_dashboard')

    job = get_object_or_404(JobOpening, id=job_id)
    job.is_active = not job.is_active
    job.save(update_fields=['is_active'])

    if job.is_active:
        messages.success(request, f'"{job.title}" is now active.')
    else:
        messages.success(request, f'"{job.title}" is now inactive.')

    return redirect('recruitment_dashboard')


# =========================
# DELETE JOB
# =========================
@login_required
def delete_job(request, job_id):
    require_hr_admin(request.user)

    job = get_object_or_404(JobOpening, id=job_id)

    if request.method == 'POST':
        title = job.title
        job.delete()
        messages.success(
            request,
            f'"{title}" and its related applications were deleted.'
        )
        return redirect('recruitment_dashboard')

    return render(
        request,
        'requirement/delete_job.html',
        {'job': job}
    )


# =========================
# ACTIVE JOB LIST + SEARCH/FILTER
# =========================
@login_required
def job_list(request):
    jobs = JobOpening.objects.filter(is_active=True)

    search = request.GET.get('search', '').strip()
    department = request.GET.get('department', '').strip()
    job_type = request.GET.get('job_type', '').strip()

    if search:
        jobs = jobs.filter(
            Q(title__icontains=search)
            | Q(department__icontains=search)
            | Q(location__icontains=search)
            | Q(description__icontains=search)
            | Q(requirements__icontains=search)
        )

    if department:
        jobs = jobs.filter(department__iexact=department)

    valid_job_types = [
        choice[0] for choice in JobOpening.JOB_TYPE_CHOICES
    ]
    if job_type in valid_job_types:
        jobs = jobs.filter(job_type=job_type)
    else:
        job_type = ''

    departments = (
        JobOpening.objects.filter(is_active=True)
        .order_by('department')
        .values_list('department', flat=True)
        .distinct()
    )

    return render(
        request,
        'requirement/job_list.html',
        {
            'jobs': jobs.order_by('-posted_on'),
            'search': search,
            'selected_department': department,
            'selected_job_type': job_type,
            'departments': departments,
            'job_types': JobOpening.JOB_TYPE_CHOICES,
        }
    )


# =========================
# APPLY FOR JOB
# =========================
@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(
        JobOpening,
        id=job_id,
        is_active=True
    )

    if request.method == 'POST':
        applicant_name = request.POST.get(
            'applicant_name', ''
        ).strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        resume_link = request.POST.get('resume_link', '').strip()
        cover_letter = request.POST.get('cover_letter', '').strip()

        if not applicant_name or not email or not phone:
            messages.error(request, 'Please fill all required fields.')
        else:
            JobApplication.objects.create(
                job=job,
                applicant_name=applicant_name,
                email=email,
                phone=phone,
                resume_link=resume_link,
                cover_letter=cover_letter
            )

            hr_admin_users = User.objects.filter(
                profile__role__in=['ADMIN', 'HR']
            )

            Notification.objects.bulk_create([
                Notification(
                    user=user,
                    title='New Job Application',
                    message=(
                        f'{applicant_name} has applied for '
                        f'the position: {job.title}.'
                    ),
                    notification_type='JOB'
                )
                for user in hr_admin_users
            ])

            messages.success(
                request,
                'Your application has been submitted successfully!'
            )
            return redirect('job_list')

    return render(
        request,
        'requirement/apply_job.html',
        {'job': job}
    )


# =========================
# APPLICATIONS MANAGEMENT
# =========================
@login_required
def application_list(request):
    require_hr_admin(request.user)

    applications = JobApplication.objects.select_related(
        'job'
    ).all()

    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()

    if search:
        applications = applications.filter(
            Q(applicant_name__icontains=search)
            | Q(email__icontains=search)
            | Q(phone__icontains=search)
            | Q(job__title__icontains=search)
        )

    valid_statuses = [
        choice[0] for choice in JobApplication.STATUS_CHOICES
    ]

    if status in valid_statuses:
        applications = applications.filter(status=status)
    else:
        status = ''

    return render(
        request,
        'requirement/application_list.html',
        {
            'applications': applications.order_by('-applied_on'),
            'status_choices': JobApplication.STATUS_CHOICES,
            'search': search,
            'selected_status': status,
        }
    )


# =========================
# UPDATE APPLICATION STATUS
# =========================
@login_required
def update_application_status(request, application_id):
    require_hr_admin(request.user)

    if request.method != 'POST':
        return redirect('application_list')

    application = get_object_or_404(
        JobApplication,
        id=application_id
    )

    new_status = request.POST.get('status', '')
    valid_statuses = [
        choice[0] for choice in JobApplication.STATUS_CHOICES
    ]

    if new_status in valid_statuses:
        application.status = new_status
        application.save(update_fields=['status'])
        messages.success(
            request,
            f'Status updated for {application.applicant_name}.'
        )
    else:
        messages.error(request, 'Invalid application status.')

    return redirect('application_list')

