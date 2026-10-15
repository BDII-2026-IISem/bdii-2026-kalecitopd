from rest_framework import serializers
from .models import Sale, SaleDetail

class SaleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetail
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    details = SaleDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = '__all__'