
from django.contrib import admin
from .models import Payroll


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'employee',
        'month',
        'year',
        'basic_salary',
        'allowances',
        'deductions',
        'net_salary',
        'payment_date',
        'is_paid',
    )

    list_filter = (
        'year',
        'month',
        'is_paid',
        'payment_date',
    )

    search_fields = (
        'employee__username',
        'employee__first_name',
        'employee__last_name',
        'employee__email',
    )

    list_editable = (
        'is_paid',
    )

    readonly_fields = (
        'net_salary',
        'created_at',
    )

    ordering = (
        '-year',
        '-month',
    )

    date_hierarchy = 'payment_date'

    list_per_page = 25