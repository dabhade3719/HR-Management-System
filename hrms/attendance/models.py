
from django.db import models
from employees.models import Employee


class Attendance(models.Model):

    STATUS_CHOICES = (
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('HALF_DAY', 'Half Day'),
        ('ON_LEAVE', 'On Leave'),
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )

    date = models.DateField()

    check_in = models.TimeField(
        null=True,
        blank=True
    )

    check_out = models.TimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PRESENT'
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'date'],
                name='unique_employee_attendance_per_day'
            )
        ]

    def __str__(self):
        return f"{self.employee} - {self.date}"

    @property
    def working_hours(self):
        if self.check_in and self.check_out:
            from datetime import datetime

            start = datetime.combine(self.date, self.check_in)
            end = datetime.combine(self.date, self.check_out)

            if end < start:
                from datetime import timedelta
                end += timedelta(days=1)

            duration = end - start
            return round(duration.total_seconds() / 3600, 2)

        return 0