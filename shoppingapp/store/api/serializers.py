from rest_framework import serializers
from store.models import Product, Categories


class ProductSerializerv1(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','image','desc','stock','price']



class ProductSerializerv2(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','desc','stock','price']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product.name','product.stock','product.price']

