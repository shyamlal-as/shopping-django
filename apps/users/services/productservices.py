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
        """
        Paginated display of products

        :param content: Products to be displayed
        :param WSGI request - request

        :return page: page containing products in paginated display
        """

        paginator=Paginator(content,6)
        page_num=request.GET.get('page')
        page=paginator.get_page(page_num)
        return(page)

    def allProducts(self,request):
        """
        Fetching all products

        :param WSGI request - request

        :return ProductServices.paginator(self,products,request):A method that returns page containing 
                                                                 products in paginated display
        """
        products=ProductServices.product.all()
        return(ProductServices.paginator(self,products,request))


    def allCategories(self,request,category_id):
        """
        Fetching all products of a category

        :param WSGI request - request
        :param category_id - Id of category to be displayed

        :return ProductServices.paginator(self,categories_id,request):A method that returns page containing 
                                                                      products of the selected category in paginated display
        """

        categories=ProductServices.product.filter(categories_id=category_id)
        return(ProductServices.paginator(self,categories,request))

    def search(self,request):
        """
        Fetching all products matching the search key

        :param WSGI request - request

        :return ProductServices.paginator(self,products,request):A method that returns page containing 
                                                                 products matching search key in paginated display
        """
        search=request.POST['search']   
        products=Product.objects.all().filter(Q(name__icontains=search))
        context={
        'page':ProductServices.paginator(self,products,request),
        'key':search,
        }
        return(context)