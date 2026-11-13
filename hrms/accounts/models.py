from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('HR', 'HR'),
        ('MANAGER', 'Manager'),
        ('EMPLOYEE', 'Employee'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='EMPLOYEE'
    )

    phone = models.CharField(max_length=15, blank=True)

    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"