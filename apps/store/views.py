import sys 
sys.path.append("..")
from django.shortcuts import render, redirect
from .models import Categories,Product
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



########Product Display Start

_productService = productservices.ProductServices()
_purchaseService = purchaseservices.PurchaseServices()

#Home Screen

def store(request):
	"""
	Homepage display
	:param WSGI request
	:return HTML render : Homepage display
	"""

	context={
		'page':_productService.allProducts(request),
	}
	return render(request,'store/store.html',context)


#Category View


def product(request,category_id):

	"""
	Displaying categorical view of products.
	:params WSGI request
	:return HTML render : HTML page that contains products of the selected category
	"""

	context={
		'page':_productService.allCategories(request,category_id)
	}

	return render(request,'store/prod.html',context)


#Search Products

def search(request):

	"""
	Displaying search results.
	:params WSGI request
	:return HTML render : Fetches all products that contain the search key as a subset.
	"""

	if request.method=='POST':
		
		context= _productService.search(request)
		
		return render(request,'store/search.html',context)
	else:
		return render(request,'store/store.html')


#Product Details

def details(request,slug):

	"""
	Displaying product details for the selected product.
	:params WSGI request
	:return HTML render : Renders a page containing the product details like name, price, description.
	"""

	product=Product.objects.filter(id=slug)
	context={
		'product':product
	}
	return render(request, 'store/details.html', context)

###### Product Display End




###Cart Views Start

#Create Cart View



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


def profile(request):
	"""
	User profile display
	:param WSGI request
	:return HTML render : A page containing user details 

	"""		
	currentUser=request.user
	display=[]
	message=""
	if currentUser.is_authenticated:
		for each in Purchases.objects.all().filter(Users_ID=currentUser,isActive=False):
			for eq in ProductPurchases.objects.filter(purchases_ID=each.id):
				display.append(eq)
		
		if len(display)==0:
			message="You have not made any purchases"
		return render(request,'store/profile.html',{'products':display,'message':message})
	else:
		messages.success(request,  'Login to continue.')
		return redirect('login')
