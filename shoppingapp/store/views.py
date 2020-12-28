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
#from constants.messages import errors,success
from constants.messages import errors,success

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
	Import the file
	Validate the input file and insert/update records

	:param Request request: Request object
	:param str import_type: Import Type
	:param str organisation_id: Uuid of organisation

	:return JsonResponse: Success/failure response
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



