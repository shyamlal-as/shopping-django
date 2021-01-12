from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
#from rest_framework.authtoken.models import Token

# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self,email,first_name,password=None):
        if not email:
            return ValueError("Users must have an email address")
        if not first_name:
            return ValueError("Users must have a name")

        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_superuser(self,email,first_name,password):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name = first_name,
            password = password,
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using = self._db)
        return user




class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email",max_length=60, unique=True)
    username = models.CharField(max_length=30,unique=True)
    date_joined = models.DateTimeField(verbose_name='date_joined',auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login',auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    first_name = models.CharField(max_length=30)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

"""
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
"""


#Profile Model for users


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    image = models.ImageField(default='user.jpg',upload_to="pics")
    age = models.IntegerField()
    

    def __str__(self):
        return str(self.user.username)