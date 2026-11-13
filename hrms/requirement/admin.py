from django.contrib import admin
from .models import JobOpening, JobApplication


@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'title',
        'department',
        'location',
        'job_type',
        'vacancies',
        'is_active',
        'posted_on',
    )

    list_filter = (
        'department',
        'job_type',
        'is_active',
    )

    search_fields = (
        'title',
        'department',
        'location',
        'description',
        'requirements',
    )

    list_editable = (
        'is_active',
    )

    readonly_fields = (
        'posted_on',
    )

    ordering = (
        '-posted_on',
    )

    list_per_page = 25


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'applicant_name',
        'job',
        'email',
        'phone',
        'status',
        'applied_on',
    )

    list_filter = (
        'status',
        'applied_on',
        'job',
    )

    search_fields = (
        'applicant_name',
        'email',
        'phone',
        'job__title',
    )

    list_editable = (
        'status',
    )

    readonly_fields = (
        'applied_on',
    )

    ordering = (
        '-applied_on',
    )

    list_per_page = 25