
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .forms import RegisterForm
from .models import Profile



def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            Profile.objects.get_or_create(
                user=user,
                defaults={'role': 'EMPLOYEE'}
            )

            messages.success(
                request,
                "Registration successful! Please login."
            )

            return redirect('login')

    else:
        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        'accounts/login.html'
    )


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'EMPLOYEE'}
    )

    if profile.role == 'ADMIN':
        return redirect('admin_dashboard')

    elif profile.role == 'HR':
        return redirect('hr_dashboard')

    elif profile.role == 'MANAGER':
        return redirect('manager_dashboard')

    elif profile.role == 'EMPLOYEE':
        return redirect('employee_dashboard')

    return HttpResponseForbidden("Invalid user role.")


@login_required
def admin_dashboard(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'EMPLOYEE'}
    )

    if profile.role != 'ADMIN':
        return HttpResponseForbidden(
            "You are not allowed to access this page."
        )

    return render(
        request,
        'accounts/admin_dashboard.html'
    )


@login_required
def hr_dashboard(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'EMPLOYEE'}
    )

    if profile.role != 'HR':
        return HttpResponseForbidden(
            "You are not allowed to access this page."
        )

    return render(
        request,
        'accounts/hr_dashboard.html'
    )


@login_required
def manager_dashboard(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'EMPLOYEE'}
    )

    if profile.role != 'MANAGER':
        return HttpResponseForbidden(
            "You are not allowed to access this page."
        )

    return render(
        request,
        'accounts/manager_dashboard.html'
    )


@login_required
def employee_dashboard(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'EMPLOYEE'}
    )

    if profile.role != 'EMPLOYEE':
        return HttpResponseForbidden(
            "You are not allowed to access this page."
        )

    return render(
        request,
        'accounts/employee_dashboard.html'
    )

@login_required
def contact_hr(request):
    return render(
        request,
        'accounts/contact_hr.html'
    )

