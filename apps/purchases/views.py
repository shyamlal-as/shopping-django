import sys 
sys.path.append("..")
from django.shortcuts import render, redirect
from store.models import Categories,Product
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator

from django.shortcuts import get_object_or_404

from purchases.models import Purchases, ProductPurchases
from users.models import Profile
from datetime import date
from django.contrib import messages

from django.utils.translation import gettext as _
from .services import productservices, purchaseservices
from purchases.models import shipping

from django.contrib.auth import login,authenticate,logout
from constants.messages import errors,success


def cart(request):

    """
    Adding a product to the cart/Creating a cart.
    :param WSGI request
    :return HTML redirect : redirects to the same page after the selected product has been added to cart
    """
    if request.user.is_authenticated:
        try:
            prod=request.GET.get('pid')
            _purchaseService.CreateCart(request,prod)
            messages.success(request,  success.ADDED_TO_CART)
            return redirect(request.META['HTTP_REFERER'])
            
        except:
            return render(request,'store/cart.html')
    
    else:
        return redirect('store')



    

def displayCart(request):

    """
    Displaying the products in the cart.
    :param WSGI request
    :return HTML render : Displays all products added to the cart
    """

    if request.user.is_authenticated:
        
        context=_purchaseService.DisplayCart(request)
        return render(request,'store/cart.html',context)
    else:
        messages.success(request,  'Login to continue.')
        return redirect('login')



def remove(request):

    """
    Removes the selected product from cart.
    :param WSGI request
    :return HTML render : The cart page with the selected product removed from cart
    """
    
    context= _purchaseService.RemoveProduct(request)    
    return render(request,'store/cart.html',context)


def clearCart(request):

    """
    Remove all products from the cart.
    :param WSGI request
    :return HTML render : Empty cart display.
    """

    _purchaseService.ClearCart(request)
    return displayCart(request)


def plus(request):

    """
    Increase quantity of a product in the cart by one.
    :params WSGI request
    :return HTML render : The cart page containing the new quantity amount.
    """
    plus=request.POST.get('id')
    context = _purchaseService.IncreaseQuantity(request,plus)
    return render(request,'store/cart.html',context)



def minus(request):

    """
    Decrease quantity of a product in the cart by one.
    :param WSGI request
    :return HTML render : The cart page containing the new quantity amount.
    """
    minus=request.POST.get('id')
    context= _purchaseService.DecreaseQuantity(request,minus)
    return render(request,'store/cart.html',context)



def complete(request):
    """
    Complete the purchase
    :param WSGI request
    :return HTML render : A page indicating a succesful purchase 

    """
    _purchaseService.Checkout(request)
    return render(request,'store/complete.html')


#Cart Views End
