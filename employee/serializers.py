from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for Employee objects.
    """
    user_email = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Employee
        fields = ['bio', 'user_email']
        read_only_fields = ['user_email']

    def get_user_email(self, obj):
        return obj.user.email

    def create(self, validated_data):
        user = self.context['request'].user
        employee, created = Employee.objects.get_or_create(
            user=user, defaults=validated_data)
        return employee
