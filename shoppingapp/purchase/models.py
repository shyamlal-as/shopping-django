from django.db import models
from users.models import User
from store.models import Product
# Create your models here.

class Purchases(models.Model):
	Users_ID=models.ForeignKey(User,related_name='Users_ID' ,default=None,on_delete=models.CASCADE)
	date=models.DateTimeField(auto_now=True)

class ProductPurchases(models.Model):
	purchases_ID=models.ForeignKey(Purchases,related_name='Purchase_ID' ,default=None,on_delete=models.CASCADE)
	product_ID=models.ForeignKey(Product,related_name='product_ID' ,default=None,on_delete=models.CASCADE)
	quantity=models.DecimalField(max_digits=3,decimal_places=1)
	price=models.DecimalField(max_digits=9,decimal_places=3)
