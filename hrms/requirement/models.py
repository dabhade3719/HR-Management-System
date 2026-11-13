from django.db import models
from django.core.validators import MinValueValidator


class JobOpening(models.Model):

    JOB_TYPE_CHOICES = [
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        ('INTERNSHIP', 'Internship'),
        ('CONTRACT', 'Contract'),
    ]

    title = models.CharField(max_length=200)

    department = models.CharField(
        max_length=100
    )

    location = models.CharField(
        max_length=150
    )

    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES,
        default='FULL_TIME'
    )

    description = models.TextField()

    requirements = models.TextField()

    salary_range = models.CharField(
        max_length=100,
        blank=True
    )

    vacancies = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1)
        ]
    )

    is_active = models.BooleanField(
        default=True
    )

    posted_on = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-posted_on']


class JobApplication(models.Model):

    STATUS_CHOICES = [
        ('APPLIED', 'Applied'),
        ('SHORTLISTED', 'Shortlisted'),
        ('INTERVIEW', 'Interview'),
        ('SELECTED', 'Selected'),
        ('REJECTED', 'Rejected'),
    ]

    job = models.ForeignKey(
        JobOpening,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    applicant_name = models.CharField(
        max_length=150
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=20
    )

    resume_link = models.URLField(
        blank=True
    )

    cover_letter = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='APPLIED'
    )

    applied_on = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.applicant_name} - {self.job.title}"

    class Meta:
        ordering = ['-applied_on']