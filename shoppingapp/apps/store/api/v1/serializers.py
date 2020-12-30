from rest_framework import serializers
from apps.store.models import Product, Categories


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','image','desc','stock','price']




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','stock','price']

