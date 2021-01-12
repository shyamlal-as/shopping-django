from django.db import models
from users.models import User
# Create your models here.

class Vendor(models.Model):
	User_ID=models.ForeignKey(User,related_name='User_ID' ,default=None,on_delete=models.CASCADE)
	Company_name=models.CharField(max_length=200)
	Company_desc=models.TextField(max_length=900)
