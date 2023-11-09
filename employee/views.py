from rest_framework import generics, permissions
from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeCreateView(generics.CreateAPIView):
    """
    View to create a new employee profile. Assumes that a user instance already exists.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmployeeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EmployeeProfileView(generics.RetrieveUpdateAPIView):
    """
    View to retrieve or update an employee's profile. Only accessible to authenticated users.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        return Employee.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset)
        return obj
