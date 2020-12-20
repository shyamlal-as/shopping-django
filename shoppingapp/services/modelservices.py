from purchases.models import Purchases, ProductPurchases
from store.models import Product, Categories
from users.models import User

from django.db.models import Q
from django.core.paginator import Paginator
from datetime import date


product=Product.objects
category=Categories.objects
purchase=Purchases.objects
productPurchase=ProductPurchases.objects

def allProducts(request):
    products=product.all()
    return(paginator(products,request))


def allCategories(request,category_id):
    categories=product.filter(categories_id=category_id)
    return(paginator(categories,request))


def paginator(content,request):
    paginator=Paginator(content,6)
    page_num=request.GET.get('page')
    page=paginator.get_page(page_num)
    return(page)


def CreateCart(request):
    prod=request.GET.get('pid')
    currentUser=request.user

    if not purchase.filter(Users_ID=currentUser.id,isActive=True).exists():
        purchaseDetail=Purchases(Users_ID=request.user,date=date.today())
        purchaseDetail.save()
        pid=product.get(id=prod)
        pr=pid.price
        purchaseProduct=ProductPurchases(purchases_ID=purchase.latest('pk'),product_ID=pid,quantity=1,price=pr)
        purchaseProduct.save()
    elif purchase.filter(Users_ID=currentUser.id,isActive=True).exists():
        print("---------------------Got in--------------")
        n=purchase.filter(Users_ID=currentUser,isActive=True).first()
        print("the needed one: ",n.id)
        if not ProductPurchases.objects.filter(product_ID=prod,purchases_ID=n.id).exists():
            prod=request.GET.get('pid')
            print('prodd----------',prod)
            pid=product.get(id=prod)
            pr=pid.price
            purchaseProduct=ProductPurchases(purchases_ID=purchase.latest('pk'),product_ID=pid,quantity=1,price=pr)
            purchaseProduct.save()
        else:
            pass			
    products=product.all().filter(categories_id=product.get(id=prod).categories_id)