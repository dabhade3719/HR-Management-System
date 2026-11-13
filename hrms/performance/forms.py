
from django import forms
from .models import PerformanceReview


class PerformanceReviewForm(forms.ModelForm):

    class Meta:
        model = PerformanceReview

        fields = [
            'employee',
            'review_period_start',
            'review_period_end',
            'rating',
            'goals_achieved',
            'strengths',
            'areas_for_improvement',
            'reviewer_feedback',
        ]

        widgets = {
            'employee': forms.Select(attrs={
                'class': 'form-select'
            }),
            'review_period_start': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'review_period_end': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select'
            }),
            'goals_achieved': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe goals achieved'
            }),
            'strengths': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Employee strengths'
            }),
            'areas_for_improvement': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Areas for improvement'
            }),
            'reviewer_feedback': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Overall performance feedback'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get('review_period_start')
        end_date = cleaned_data.get('review_period_end')

        if start_date and end_date and end_date < start_date:
            self.add_error(
                'review_period_end',
                'Review end date cannot be before start date.'
            )

        return cleaned_data