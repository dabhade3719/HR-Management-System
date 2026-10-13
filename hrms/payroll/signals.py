from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Payroll
from notifications.models import Notification


@receiver(post_save, sender=Payroll)
def payroll_notification(sender, instance, created, **kwargs):

    if created:
        Notification.objects.create(
            user=instance.employee,
            title="New Payroll Available",
            message=(
                f"Your payroll for "
                f"{instance.month}/{instance.year} "
                f"has been generated."
            ),
            notification_type="PAYROLL"
        )