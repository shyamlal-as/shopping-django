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
from.services import productservice
from purchases.models import shipping

from django.contrib.auth import login,authenticate,logout



########Product Display Start

_productService = productservice.ProductService()

#Home Screen

def store(request):
	"""
	Fetch all the products from Products table
	Display in a template

	:param WSGI Request request: Request object
	:param str import_type: Import Type
	:param str organisation_id: Uuid of organisation

	:return render: html template
	"""

	context={
		'page':_productService.allProducts(request),
	}
	return render(request,'store/store.html',context)


#Category View


def product(request,category_id):

	"""
	Fetch the products with the given category id
	Display in a template

	:param WSGI Request request: Request object
	:param slug category_id: Category id

	:return render: html template
	"""

	context={
		'page':_productService.allCategories(request,category_id)
	}

	return render(request,'store/prod.html',context)


#Search Products

def search(request):

	"""
	Fetch the products with names matching search key
	Display in a template

	:param WSGI Request request: Request object

	:return render: html template
	"""

	if request.method=='POST':
		
		context= _productService.search(request)
		
		return render(request,'store/search.html',context)
	else:
		return render(request,'store/store.html')


#Product Details

def details(request,slug):

	"""
	Fetch the details of the product with given product id
	Display in a template

	:param WSGI Request request: Request object
	:param slug slug: Product id

	:return render: html template
	"""

	product=Product.objects.filter(id=slug)
	context={
		'product':product
	}
	return render(request, 'store/details.html', context)



def profile(request):

	"""
	Fetch the details of the user and previous orders
	Display in a template

	:param WSGI Request request: Request object

	:return render: html template
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



