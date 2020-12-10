from django.db import models
from purchase.models import Purchases 
from users.models import User
# Create your models here.

class shipping(models.Model):
	Users_ID=models.ForeignKey(User,related_name='UserID' ,default=None,on_delete=models.PROTECT)
	address=models.TextField(max_length=200)
	city=models.TextField(max_length=200)
	pincode=models.IntegerField()
