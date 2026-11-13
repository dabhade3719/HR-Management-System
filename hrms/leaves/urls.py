
from django.urls import path
from . import views

urlpatterns = [
    # Employee
    path('apply/', views.apply_leave, name='apply_leave'),
    path('my/', views.my_leaves, name='my_leaves'),

    # HR / Admin
    path('manage/', views.manage_leaves, name='manage_leaves'),
    path('review/<int:id>/', views.review_leave, name='review_leave'),
]