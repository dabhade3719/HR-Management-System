
from django.contrib import admin
from .models import PerformanceReview


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):

    list_display = (
        'employee',
        'reviewer',
        'review_period_start',
        'review_period_end',
        'rating',
        'created_at',
    )

    list_filter = (
        'rating',
        'review_period_start',
        'review_period_end',
    )

    search_fields = (
        'employee__first_name',
        'employee__last_name',
        'employee__employee_id',
        'reviewer__username',
        'reviewer__email',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    date_hierarchy = 'created_at'