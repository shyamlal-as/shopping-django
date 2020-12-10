from django.contrib import admin
from .models import Purchases, ProductPurchases


# Register your models here.


class PurchasesAdmin(admin.ModelAdmin):
    list_display = ('id','Users_ID','date','isActive')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(ProductPurchases)
admin.site.register(Purchases,PurchasesAdmin)

