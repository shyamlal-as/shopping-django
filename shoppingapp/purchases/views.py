from django.shortcuts import render, redirect
from .models import Purchases, ProductPurchases
from store.models import Categories,Product
from django.contrib import messages


from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator

from django.shortcuts import get_object_or_404

from users.models import Profile
from datetime import date
from constants.messages import errors,success

from django.utils.translation import gettext as _
from services import modelservices, productservices, purchaseservices
from purchases.models import shipping




_productService = productservices.ProductServices()
_purchaseService = purchaseservices.PurchaseServices()

def cart(request):

	"""
	@desc : Adding a product to the cart.
	@params WSGI request
	@return HTML redirect :
				If Purchases table has an entry with current userId and isActive attribute true: 
					Add the product and quantity to ProductPurchases table,
				Else:
					Add an entry to Purchases table and ProductPurchases table.
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
	@desc : Displaying the products in the cart.
	@params WSGI request
	@return HTML render : Fetches entries from ProductPurchases table which has
						  purchasesId as the entry from Purchases table with
						  current userId and isActive true.
	"""

	if request.user.is_authenticated:
		
		context=_purchaseService.DisplayCart(request)
		return render(request,'store/cart.html',context)
	else:
		messages.success(request,  'Login to continue.')
		return redirect('login')



def remove(request):

	"""
	@desc : Removes a certain product from cart.
	@params WSGI request
	@return HTML render : Deletes the respective entry from ProductPurchases table
						  and renders cart.html.
	"""
	
	context= _purchaseService.RemoveProduct(request)	
	return render(request,'store/cart.html',context)


def clearCart(request):

	"""
	@desc : Clear the cart of all products.
	@params WSGI request
	@return HTML render :Deletes the entry from Purchases table and renders cart.html.
	"""

	_purchaseService.ClearCart(request)
	return displayCart(request)


def plus(request):

	"""
	@desc : Increase quantity of a product in the cart by one.
	@params WSGI request
	@return HTML render : Increments quantity attribute of ProductPurchases table
						  and renders Cart page.
	"""
	plus=request.POST.get('id')
	context = _purchaseService.IncreaseQuantity(request,plus)
	return render(request,'store/cart.html',context)



def minus(request):

	"""
	@desc : Decrease quantity of a product in cart by one.
	@params WSGI request
	@return HTML render : Decrement quantity attribute of ProductPurchases table
						  and renders Cart page.
	"""
	minus=request.POST.get('id')
	context= _purchaseService.DecreaseQuantity(request,minus)
	return render(request,'store/cart.html',context)



def complete(request):
	_purchaseService.Checkout(request)
	return render(request,'store/complete.html')

