from django.contrib import admin
from .models import Purchases, ProductPurchases,shipping


# Register your models here.


class PurchasesAdmin(admin.ModelAdmin):
    list_display = ('id','Users_ID','date','isActive')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class ProductPurchasesAdmin(admin.ModelAdmin):
    model=ProductPurchases
    list_display=('id','purchases_ID','product_ID','quantity','price')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(ProductPurchases,ProductPurchasesAdmin)
admin.site.register(Purchases,PurchasesAdmin)
admin.site.register(shipping)

