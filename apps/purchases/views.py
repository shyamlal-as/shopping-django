from django.shortcuts import render, redirect
from .models import Purchases, ProductPurchases
from store.models import Product
from django.contrib import messages

from django.db.models import Q

import logging
logger = logging.getLogger(__name__)


def add_to_cart(request, slug):

    criterion1 = Q(Users_ID=request.user)
    criterion2 = Q(isActive=True)

    q = Purchases.objects.filter(criterion1 & criterion2).exists()


    if(q):
        prod_Purchases(slug)
        messages.info(request,"Added to cart")
        return redirect('store')
    else:
        cart = Purchases(Users_ID=request.user)
        cart.save()
        prod_Purchases(slug)
        messages.info(request,"Added to cart")
        return redirect('store')


def prod_Purchases(slug):

    product = Product.objects.filter(id=slug).first()
    cart = Purchases.objects.order_by('-pk')[0]
    prod= ProductPurchases(purchases_ID=cart, product_ID=product, quantity="1.0", price="234.5")
    prod.save()

    

def cart(request):

    criterion1 = Q(Users_ID=request.user)
    criterion2 = Q(isActive=True)
    q = Purchases.objects.get(criterion1 & criterion2)
    purchId=q.id
    purchase = ProductPurchases.objects.filter(purchases_ID=purchId)
    prod= ProductPurchases.objects.select_related('product_ID').filter(purchases_ID=purchId)
    #prod= Product.objects.filter(followers__country__name='Bulgaria')
    #prodId = ProductPurchases.objects.filter(purchases_ID=purchId).first().product_ID.id
    
    #product = Product.objects.filter(id=prodId)

    context = {'purchases':purchase, 'products':prod}
    return render(request,'store/cart.html',context)