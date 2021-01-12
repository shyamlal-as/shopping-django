from django.contrib import admin
from .models import Vendor
# Register your models here.


class VendorAdmin(admin.ModelAdmin):
    list_display=('Company_name','Company_desc')


admin.site.register(Vendor,VendorAdmin)