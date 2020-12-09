from django.db import models
from users.models import User
from store.models import Product
# Create your models here.

class Purchases(models.Model):
	Users_ID=models.ForeignKey(User,related_name='Users_ID' ,default=None,on_delete=models.CASCADE)
	date=models.DateTimeField(auto_now=True)
	isActive=models.BooleanField(default=True)

class ProductPurchases(models.Model):
	purchases_ID=models.ForeignKey(Purchases,related_name='Purchase_ID' ,default=None,on_delete=models.CASCADE)
	product_ID=models.ForeignKey(Product,related_name='Product_ID' ,default=None,on_delete=models.CASCADE)
	quantity=models.IntegerField()
	price=models.DecimalField(max_digits=9,decimal_places=3)
