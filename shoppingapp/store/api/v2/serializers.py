from rest_framework import serializers
from store.models import Product, Categories



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','desc','stock','price']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','stock','price']

