from rest_framework import serializers
from apps.purchases.models import Purchases, ProductPurchases


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchases
        fields = []


class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPurchases
        fields=[]



class ConfirmPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchases
        fields=['isActive']

