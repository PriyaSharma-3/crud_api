# employee_api/urls.py
from django.urls import path
from .views import create_employee, update_employee, get_employee, delete_employee

urlpatterns = [
    path('create/', create_employee, name='create_employee'),
    path('update/<int:id>/', update_employee, name='update_employee'),
    path('get_all/', get_employee, name='get_all_employees'),
    path('delete/<int:id>/', delete_employee, name='delete_employee'),
    path('get_employee/<str:id>/', get_employee, name='get_single_employee'),
]
