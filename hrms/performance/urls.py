
from django.urls import path
from . import views

urlpatterns = [
    path('', views.performance_list, name='performance_list'),
    path('create/', views.performance_create, name='performance_create'),
    path('<int:pk>/', views.performance_detail, name='performance_detail'),
]