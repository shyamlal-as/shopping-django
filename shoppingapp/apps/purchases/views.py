from django.shortcuts import render, redirect
from .models import Purchases, ProductPurchases
from apps.store.models import Categories,Product
from django.contrib import messages


from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404

from datetime import date
from constants.messages import errors,success

from django.utils.translation import gettext as _
from .services import purchaseservice

from apps.purchases.models import shipping


_purchaseService = purchaseservice.PurchaseService()

def cart(request):

	"""
	Add a product to cart

	:param WSGI Request request: Request object

	:return redirect: Redirect to the same page
	"""
	if request.user.is_authenticated:
		try:
			prod=request.GET.get('pid')
			_purchaseService.CreateCart(request,prod)
			msg = success.ADDED_TO_CART
			messages.success(request, msg)
			return redirect(request.META['HTTP_REFERER'])
			
		except:
			return render(request,'store/cart.html')
	
	else:
		#msg = success.ADDED_TO_CART
		#messages.success(request,  'Login to continue')
		return redirect('profile')



	

def displayCart(request):

	"""
	Display the current projects in the cart

	:param WSGI Request request: Request object

	:return render: html template
	"""

	if request.user.is_authenticated:
		
		context=_purchaseService.DisplayCart(request)
		return render(request,'store/cart.html',context)
	else:
		message= errors.LOGIN_REQUIRED
		messages.success(request,  message)
		return redirect('login')



def remove(request):

	"""
	Remove a product from cart

	:param WSGI Request request: Request object

	:return render: html template
	"""
	
	context= _purchaseService.RemoveProduct(request)	
	return render(request,'store/cart.html',context)


def clearCart(request):


	"""
	Clear the current cart

	:param WSGI Request request: Request object

	:return render: html template
	"""

	_purchaseService.ClearCart(request)
	return displayCart(request)


def plus(request):

	"""
	Increase quantity of a product in the cart

	:param WSGI Request request: Request object

	:return render: html template
	"""

	plus=request.POST.get('id')
	context = _purchaseService.IncreaseQuantity(request,plus)
	return render(request,'store/cart.html',context)



def minus(request):

	"""
	Decrease quantity of a product in the cart

	:param WSGI Request request: Request object

	:return render: html template
	"""

	minus=request.POST.get('id')
	context= _purchaseService.DecreaseQuantity(request,minus)
	return render(request,'store/cart.html',context)



def complete(request):

	"""
	Complete the checkout

	:param WSGI Request request: Request object

	:return render: html template
	"""

	_purchaseService.Checkout(request)
	return render(request,'store/complete.html')

