# employee_api/views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Employee
from .serializers import EmployeeSerializer
import json

@api_view(['POST'])
def create_employee(request):
    try:
        # Check if email is unique
        email = request.data.get('email')
        if Employee.objects.filter(email=email).exists():
            # Duplicate email found
            return Response({'message': 'Employee with this email already exists', 'success': False}, status=status.HTTP_200_OK)

        # Your serializer should have a uniqueness constraint on the email field
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            # Save employee if email is not duplicate
            employee = serializer.save()

            # Construct success response
            response_data = {
                'message': 'Employee created successfully',
                'regid': employee.id,  # Assuming id is a field in your Employee model
                'success': True,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        # If serializer is not valid
        return Response({'message': 'Invalid data', 'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Exception during employee creation
        return Response({'message': 'Employee creation failed', 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def get_employee(request, id=None):  # Use 'id' as the parameter name
    try:
        if id:
            # Single employee request
            employee = Employee.objects.filter(id=id).first()

            if employee:
                serializer = EmployeeSerializer(employee)
                response_data = {
                    'message': 'Employee details found',
                    'success': True,
                    'employees': [serializer.data]
                }
            else:
                response_data = {
                    'message': 'Employee details not found',
                    'success': False,
                    'employees': []
                }
        else:
            # All employee request
            employees = Employee.objects.all()
            serializer = EmployeeSerializer(employees, many=True)
            response_data = {
                'message': 'Employee details found',
                'success': True,
                'employees': serializer.data
            }

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        # Exception during employee retrieval
        return Response({'message': 'Error retrieving employee details', 'success': False, 'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_employee(request, id):
    try:
        # Attempt to retrieve the employee with the given id
        employee = Employee.objects.get(id=id)

        # Validate and update employee details using the provided data
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Success response for valid update
            response_data = {
                "message": "Employee details updated successfully",
                "success": True
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # Response when the provided data is invalid
            response_data = {
                "message": "Employee details updation failed",
                "success": False
            }
            return Response(response_data, status=status.HTTP_200_OK)

    except Employee.DoesNotExist:
        # Response when no employee is found with the given id
        response_data = {
            "message": "No employee found with this id",
            "success": False
        }
        return Response(response_data, status=status.HTTP_200_OK)

    except ValueError:
        # Response when there's an invalid body request (e.g., missing or incorrect data)
        response_data = {
            "message": "Invalid body request.",
            "success": False
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Response for other unexpected exceptions
        response_data = {
            "message": "Employee updation failed",
            "success": False
        }
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_employee(request,id):
    try:
        # Check if the employee with the given regid exists
        try:
            employee = Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            return Response({'message': 'No employee found with this id', 'success': False}, status=status.HTTP_200_OK)

        # Attempt to delete the employee
        try:
            employee.delete()
            return Response({'message': 'Employee deleted successfully', 'success': True}, status=status.HTTP_200_OK)
        except Exception as deletion_error:
            # Handle the case where employee deletion fails due to exception
            return Response({'message': 'Employee deletion failed', 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        # Handle other exceptions
        return Response({'message': 'employee deleted failed', 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)