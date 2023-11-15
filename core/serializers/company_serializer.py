from rest_framework import serializers
from core.models import Company


class CompanySerializer(serializers.Serializer):
    name = serializers.CharField()
    cnpj = serializers.CharField(max_length=14)
    address = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=2)
    country = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Company.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.cnpj = validated_data.get('cnpj', instance.cnpj)
        instance.address = validated_data.get('address', instance.address)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.country = validated_data.get('country', instance.country)
        instance.save()

        return instance


    class Meta:
        model = Company
        fields = ['name', 'cnpj', 'address', 'city', 'state', 'country']
