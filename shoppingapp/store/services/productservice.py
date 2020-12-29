from purchases.models import Purchases, ProductPurchases
from store.models import Product, Categories
from users.models import User

from django.db.models import Q
from django.core.paginator import Paginator
from datetime import date


class ProductService:

    product=Product.objects
    category=Categories.objects
    purchase=Purchases.objects
    productPurchase=ProductPurchases.objects


    def paginator(self,content,request):
        
        """
        Display the given content as 6 div per page

        :param WSGI Request request: Request object
        :param Query Set content: Query set containing products

        :return Page: Formatted page
        """

        paginator=Paginator(content,6)
        page_num=request.GET.get('page')
        page=paginator.get_page(page_num)
        return(page)

    def allProducts(self,request):

        """
        Fetch all the products from Products table

        :param WSGI Request request: Request object

        :return QuerySet: Formatted queryset of product list
        """

        products=self.product.order_by('-id')
        return(self.paginator(products,request))


    def allCategories(self,request,category_id):

        """
        Fetch the products with the given category id

        :param WSGI Request request: Request object
        :param slug category_id: Category id

        :return QuerySet: Formatted queryset of product list
        """

        categories=self.product.filter(categories_id=category_id).order_by('id')
        return(self.paginator(categories,request))

    def search(self,request):

        """
        Fetch the products with names matching the search key

        :param WSGI Request request: Request object

        :return QuerySet: Formatted queryset of product list
        """

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