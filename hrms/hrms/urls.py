"""
URL configuration for hrms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.shortcuts import render, redirect

urlpatterns = [
    path('', lambda request: render(request, 'home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('departments.urls')),
    path('', include('employees.urls')),
    path('', include('attendance.urls')),
    path('leaves/', include('leaves.urls')),
    path('payroll/', include('payroll.urls')),
    path('requirement/', include('requirement.urls')),
    path('notifications/', include('notifications.urls')),
    path('performance/', include('performance.urls')),
] 

handler403 = 'hrms.views.custom_permission_denied'


