
from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):

    first_name = forms.CharField(max_length=100, label="First Name")

    last_name = forms.CharField(max_length=100, label="Last Name")

    phone = forms.CharField(max_length=15, label="Phone")

    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password"
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This username is already taken."
            )

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email is already registered."
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error(
                'confirm_password',
                "Passwords do not match."
            )

        return cleaned_data