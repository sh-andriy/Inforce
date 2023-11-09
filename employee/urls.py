from django.urls import path
from .views import EmployeeCreateView, EmployeeProfileView

urlpatterns = [
    path('create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('profile/', EmployeeProfileView.as_view(), name='employee-profile'),
]
