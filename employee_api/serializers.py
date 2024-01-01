# employee_api/serializers.py
from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def validate(self, data):
            # Check data types
            expected_data_types = {
                'name': str,
                'email': str,
                'age': int,
                'gender': str,
                'phone_no': str,
                'address_details': dict,
                'work_experience': list,
                'qualifications': list,
                'projects': list,
            }

            for key, expected_type in expected_data_types.items():
                if key in data and not isinstance(data[key], expected_type):
                    raise serializers.ValidationError(f"{key} should be of type {expected_type.__name__}")

            # Check required parameters
            required_params = ['name', 'email', 'age', 'gender', 'phone_no', 'address_details', 'work_experience', 'qualifications', 'projects']
            for param in required_params:
                if param not in data:
                    raise serializers.ValidationError(f"{param} is required")

            return data