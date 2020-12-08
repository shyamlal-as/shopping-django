from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Categories(models.Model):
	name=models.CharField(max_length=100)
	desc=models.CharField(max_length=200)
	image=models.ImageField(upload_to='pics',default='default.jpg')

	def __str__(self):
		return self.name

	def get_products(self):
		return Product.objects.filter(categories=self.name)

class Product(models.Model):
	name=models.CharField(max_length=100)
	desc=models.CharField(max_length=200)
	categories_id=models.ForeignKey(Categories,related_name='Categories' ,default=None,on_delete=models.CASCADE)
	price=models.DecimalField(max_digits=11, decimal_places=3)
	image=models.ImageField(upload_to='pics',default='default.jpg')
	quantity=models.IntegerField(default=1)

	def __str__(self):
		return self.name

	def get_all_products():
		return Product.objects.all()

	def get_all_products_by_category_id(categories_id):
		if categories_id:
			return Product.objects.filter(category=categories_id)
		else:
			return Products.get_all_products()