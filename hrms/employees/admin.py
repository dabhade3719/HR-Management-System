from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        'employee_id',
        'first_name',
        'last_name',
        'department',
        'designation',
        'salary',
        'employment_status',
    )

    list_filter = (
        'department',
        'employment_status',
        'gender',
    )

    search_fields = (
        'employee_id',
        'first_name',
        'last_name',
        'email',
        'phone',
    )
