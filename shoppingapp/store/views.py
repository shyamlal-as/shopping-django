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
from services import modelservices, productservices, purchaseservices
from purchases.models import shipping

from django.contrib.auth import login,authenticate,logout



########Product Display Start

_productService = productservices.ProductServices()
_purchaseService = purchaseservices.PurchaseServices()

#Home Screen

def store(request):

	"""
	@desc : Displaying products in Home page.
	@params WSGI request
	@return HTML render : Fetches all entries of Product table and renders
						  on store.html.
	"""

	context={
		'page':_productService.allProducts(request),
	}
	return render(request,'store/store.html',context)


#Category View


def product(request,category_id):

	"""
	@desc : Displaying products in a certain category.
	@params WSGI request
	@return HTML render : Fetches products from Product table with categories_id
						  as selected and renders on prod.html.
	"""

	context={
		'page':_productService.allCategories(request,category_id)
	}

	return render(request,'store/prod.html',context)


#Search Products

def search(request):

	"""
	@desc : Displaying products matching the search key.
	@params WSGI request
	@return HTML render : Fetches products from Product table according to the 
						  search key entered.
	"""

	if request.method=='POST':
		
		context= _productService.search(request)
		
		return render(request,'store/search.html',context)
	else:
		return render(request,'store/store.html')


#Product Details

def details(request,slug):

	"""
	@desc : Displaying details of selected product.
	@params WSGI request
	@return HTML render : Renders a page with name, image, and details of 
						  a product from Product table.
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
	@desc : Adding a product to the cart.
	@params WSGI request
	@return HTML redirect :
				If Purchases table has an entry with current userId and isActive attribute true: 
					Add the product and quantity to ProductPurchases table,
				Else:
					Add an entry to Purchases table and ProductPurchases table.
	"""
	print('----------------fn-------------')
	if request.user.is_authenticated:
		try:
			print('----------In----------------------')
			prod=request.GET.get('pid')
			_purchaseService.CreateCart(request,prod)
			messages.success(request,  'added To Cart.')
			return redirect(request.META['HTTP_REFERER'])
			
		except:
			print('----------------ex-------------')
			return render(request,'store/cart.html')
	
	else:
		messages.success(request,  'added To Cart.')
		return redirect('store')



	

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
	
	context = _purchaseService.IncreaseQuantity(request)
	return render(request,'store/cart.html',context)



def minus(request):

	"""
	@desc : Decrease quantity of a product in cart by one.
	@params WSGI request
	@return HTML render : Decrement quantity attribute of ProductPurchases table
						  and renders Cart page.
	"""
	
	context= _purchaseService.DecreaseQuantity(request)
	return render(request,'store/cart.html',context)



def complete(request):
	_purchaseService.Checkout(request)
	return render(request,'store/complete.html')


#Cart Views End


def profile(request):
		
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



