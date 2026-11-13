
from django.db import models
from django.contrib.auth.models import User
from employees.models import Employee


class PerformanceReview(models.Model):

    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Needs Improvement'),
        (3, '3 - Meets Expectations'),
        (4, '4 - Exceeds Expectations'),
        (5, '5 - Outstanding'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='performance_reviews'
    )

    reviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='given_performance_reviews'
    )

    review_period_start = models.DateField()
    review_period_end = models.DateField()

    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES
    )

    goals_achieved = models.TextField()
    strengths = models.TextField()
    areas_for_improvement = models.TextField()
    reviewer_feedback = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee} - Rating: {self.rating}/5"