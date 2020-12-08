from django.contrib import admin
from .models import Categories,Product
from purchase.models import Purchases, ProductPurchases
# Register your models here.

admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(Purchases)
admin.site.register(ProductPurchases)