
from django import forms
from .models import Attendance


class AttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance

        fields = [
            'employee',
            'date',
            'check_in',
            'check_out',
            'status',
            'remarks',
        ]

        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'check_in': forms.TimeInput(
                attrs={'type': 'time', 'class': 'form-control'}
            ),
            'check_out': forms.TimeInput(
                attrs={'type': 'time', 'class': 'form-control'}
            ),
            'employee': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'status': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'remarks': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),
        }