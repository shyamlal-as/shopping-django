from django.db import models
from users.models import User
# Create your models here.

class Categories(models.Model):
	name=models.CharField(max_length=100)
	desc=models.CharField(max_length=200)
	image=models.ImageField(upload_to='pics',default='default.jpg')

class Product(models.Model):
	name=models.CharField(max_length=25)
	desc=models.CharField(max_length=200)
	stock=models.IntegerField()
	categories_id=models.ForeignKey(Categories, default=None,on_delete=models.CASCADE)
	price=models.DecimalField(max_digits=11, decimal_places=3)
	image=models.ImageField(upload_to='pics',default='default.jpg')
	isApproved=models.BooleanField(default=False)
	User_ID=models.ForeignKey(User,related_name='UID' ,default=None,on_delete=models.CASCADE)