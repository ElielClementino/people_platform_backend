from rest_framework import serializers
from core.models import CostCenter, Company, Department, Employee
from core.serializers.company_serializer import CompanySerializer
from core.serializers.cost_center_serializer import CostCenterSerializer
from core.serializers.department_serializer import DepartmentSerializer


class EmployeeSerializer(serializers.Serializer):
    company = CompanySerializer()
    department = DepartmentSerializer()
    full_name = serializers.CharField(max_length=125)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=25)
    birth_date = serializers.DateField()
    entry_date = serializers.DateField()
    departure_date = serializers.DateField()
    city = serializers.CharField(max_length=100)

    company_obj = {}
    department_obj = {}
    employee_obj = {}
    cost_center_obj = {}

    def create(self, validated_data):
        if 'company' in validated_data and 'department' in validated_data:
            company_data = validated_data.pop('company')
            department_data = validated_data.pop('department')
            cost_center_data = department_data.pop('cost_center', {})

            company_data_for_cost_center = cost_center_data.pop('company', {})

            company_obj = Company.objects.create(**company_data)
            cost_center_data.update(company=company_obj)
            cost_center_obj = CostCenter.objects.create(**cost_center_data)

            department_data.pop('company', None)
            department_obj = Department.objects.create(company=company_obj, cost_center=cost_center_obj, **department_data)

        validated_data.pop('company', None)
        validated_data.pop('cost_center', None)
        validated_data.pop('department', None)
        employee = Employee.objects.create(company=company_obj, department=department_obj, **validated_data)

        return employee

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.entry_date = validated_data.get('entry_date', instance.entry_date)
        instance.departure_date = validated_data.get('departure_date', instance.departure_date)
        instance.city = validated_data.get('city', instance.city)
        instance.save()

        return instance
