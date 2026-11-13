
from django.db import models
from django.contrib.auth.models import User


class LeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('CASUAL', 'Casual Leave'),
        ('SICK', 'Sick Leave'),
        ('PAID', 'Paid Leave'),
        ('UNPAID', 'Unpaid Leave'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='leave_requests'
    )
    leave_type = models.CharField(
        max_length=20,
        choices=LEAVE_TYPE_CHOICES
    )
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    applied_on = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_leave_requests'
    )
    review_comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type} - {self.status}"

    class Meta:
        ordering = ['-applied_on']

