from django.contrib import admin
from .models import Product, Categories



# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display=('name','desc','stock','isApproved')
    #search_fields = ['name','categories_id']

class CategoriesAdmin(admin.ModelAdmin):
    list_display=('name','desc','id')
    #search_fields = ('name')



admin.site.register(Product,ProductAdmin)
admin.site.register(Categories,CategoriesAdmin)
