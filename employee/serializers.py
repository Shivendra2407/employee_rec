from rest_framework import serializers
from .models import Employee


class EmployeeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ('name', "pan_number", "age", "gender", "email", "city",)
