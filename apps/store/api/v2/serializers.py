from rest_framework import serializers
from store.models import Product, Categories


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','image','desc','stock','price']




class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','stock','price']