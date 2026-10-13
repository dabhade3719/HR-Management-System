
from django import forms
from django.contrib.auth.models import User

from .models import Employee


class EmployeeForm(forms.ModelForm):

    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter existing username'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password for new user'
        }),
        required=False
    )

    class Meta:
        model = Employee

        fields = [
            'employee_id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'profile_photo',
            'department',
            'designation',
            'joining_date',
            'date_of_birth',
            'gender',
            'salary',
            'address',
            'employment_status',
        ]

        widgets = {
            'joining_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'address': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Enter full address'
            }),
            'salary': forms.NumberInput(attrs={
                'placeholder': 'Enter salary',
                'step': '0.01'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.is_edit = kwargs.get('instance') is not None

        super().__init__(*args, **kwargs)

        if self.is_edit:
            self.fields.pop('username')
            self.fields.pop('password')

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not self.is_edit and not User.objects.filter(
            username=username
        ).exists():
            raise forms.ValidationError(
                'This username does not exist. Register the user first.'
            )

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        existing_users = User.objects.filter(email=email)

        if self.is_edit:
            existing_users = existing_users.exclude(
                employee=self.instance
            )

        if existing_users.exists():
            # Existing linked user may already have the same email.
            if not (
                self.is_edit
                and self.instance.user.email == email
            ):
                raise forms.ValidationError(
                    'This email is already registered.'
                )

        return email