from rest_framework import serializers
from core.models import CostCenter, Company
from core.serializers.company_serializer import CompanySerializer


class CostCenterSerializer(serializers.Serializer):
    company = CompanySerializer()
    code = serializers.CharField(max_length=10)
    description = serializers.CharField(max_length=100)
    cost = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    company_data = {}

    def create(self, validated_data):
        if 'company' in validated_data:
            company_data = validated_data.pop('company')
        if company_data:
            company = Company.objects.create(**company_data)
            cost_center = CostCenter.objects.create(company=company, **validated_data)
        return cost_center

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.description = validated_data.get('description', instance.description)
        instance.cost = validated_data.get('cost', instance.cost)
        instance.save()

        return instance
