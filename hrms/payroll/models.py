
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Payroll(models.Model):

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payroll_records'
    )

    month = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(12)
        ]
    )

    year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(2000),
            MaxValueValidator(2100)
        ]
    )

    basic_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    allowances = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )

    deductions = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )

    net_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_date = models.DateField(
        null=True,
        blank=True
    )

    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.net_salary = (
            self.basic_salary
            + self.allowances
            - self.deductions
        )

        if self.net_salary < 0:
            self.net_salary = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.username} - {self.month}/{self.year}"

    class Meta:
        ordering = ['-year', '-month']

        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'month', 'year'],
                name='unique_employee_payroll_month'
            )
        ]