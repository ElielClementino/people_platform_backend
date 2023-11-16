from rest_framework import serializers
from core.models import CostCenter, Company, Department
from core.serializers.company_serializer import CompanySerializer
from core.serializers.cost_center_serializer import CostCenterSerializer


class DepartmentSerializer(serializers.Serializer):

    company = CompanySerializer()
    cost_center = CostCenterSerializer()
    name = serializers.CharField(max_length=100)
    integration_code = serializers.CharField(max_length=100)

    company_obj = {}
    cost_center_obj = {}

    def create(self, validated_data):
        if 'company' in validated_data and 'cost_center' in validated_data:
            cost_center_data = validated_data.pop('cost_center')
            company_data = cost_center_data.pop('company')
            company_obj = Company.objects.create(**company_data)
            cost_center_obj = CostCenter.objects.create(company=company_obj, **cost_center_data)

        validated_data.pop('company', None)
        validated_data.pop('cost_center', None)
        department = Department.objects.create(company=company_obj, cost_center=cost_center_obj, **validated_data)

        return department

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.integration_code = validated_data.get('integration_code', instance.integration_code)
        instance.save()

        return instance
