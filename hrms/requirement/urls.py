from django.urls import path
from . import views

urlpatterns = [
    path('', views.recruitment_dashboard, name='recruitment_dashboard'),

    # Jobs
    path('jobs/', views.job_list, name='job_list'),
    path('create/', views.create_job, name='create_job'),
    path('jobs/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('jobs/<int:job_id>/toggle/', views.toggle_job_status, name='toggle_job_status'),
    path('jobs/<int:job_id>/delete/', views.delete_job, name='delete_job'),

    # Applications
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('applications/', views.application_list, name='application_list'),
    path('applications/<int:application_id>/update/', views.update_application_status, name='update_application_status'),
]