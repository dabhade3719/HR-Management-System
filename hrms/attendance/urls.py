
from django.urls import path
from . import views

urlpatterns = [
    # Attendance List
    path('attendance/', views.attendance_list, name='attendance_list'),
    # Add Attendance
    path('attendance/add/', views.attendance_create, name='attendance_create'),
    # Edit Attendance
    path('attendance/<int:id>/edit/', views.attendance_update, name='attendance_update'),
    # Delete Attendance
    path('attendance/<int:id>/delete/', views.attendance_delete, name='attendance_delete'),

    # Employee Self Check-in / Check-out
    path('my-attendance/', views.employee_attendance, name='employee_attendance'),
    path('attendance/report/', views.attendance_report, name='attendance_report'),
]

