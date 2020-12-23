from purchases.models import Purchases, ProductPurchases
from store.models import Product, Categories
from users.models import User

from django.db.models import Q
from django.core.paginator import Paginator
from datetime import date


class ProductServices:

    product=Product.objects
    category=Categories.objects
    purchase=Purchases.objects
    productPurchase=ProductPurchases.objects


    def paginator(self,content,request):
        paginator=Paginator(content,6)
        page_num=request.GET.get('page')
        page=paginator.get_page(page_num)
        return(page)

    def allProducts(self,request):
        products=ProductServices.product.order_by('-id')
        return(ProductServices.paginator(self,products,request))


    def allCategories(self,request,category_id):
        categories=ProductServices.product.filter(categories_id=category_id).order_by('id')
        return(ProductServices.paginator(self,categories,request))

    def search(self,request):
        search=request.POST['search']	
        products=Product.objects.filter(Q(name__icontains=search)).order_by('id')
        product_paginator=Paginator(products,6)
        page_num=request.GET.get('page')
        page=product_paginator.get_page(page_num)
        context={
        'page':page,
        'key':search,
        }
        return(context)