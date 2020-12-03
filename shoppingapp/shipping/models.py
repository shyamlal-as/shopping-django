from django.db import models
from purchase.models import Purchases 
# Create your models here.

class shipping(models.Model):
	purchases_ID=models.ForeignKey(Purchases,related_name='purchases_ID',default=None,on_delete=models.CASCADE)
	address=models.TextField(max_length=200)
	city=models.TextField(max_length=200)
	pincode=models.IntegerField()
