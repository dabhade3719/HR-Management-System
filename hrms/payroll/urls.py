
from django.urls import path
from . import views

urlpatterns = [
    path('', views.payroll_list, name='payroll_list'),
    path('my/', views.my_payroll, name='my_payroll'),
]

