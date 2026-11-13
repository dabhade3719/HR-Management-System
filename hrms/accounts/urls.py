from django.urls import path
from . import views


urlpatterns = [

    path(
        'register/',
        views.register_view,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
        'dashboard/',
        views.dashboard_view,
        name='dashboard'
    ),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('hr-dashboard/', views.hr_dashboard, name='hr_dashboard'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('contact-hr/', views.contact_hr, name='contact_hr'),
]