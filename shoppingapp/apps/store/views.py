from django.shortcuts import render, redirect
from .models import Categories,Product
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator

from django.shortcuts import get_object_or_404

from apps.purchases.models import Purchases, ProductPurchases
from apps.users.models import Profile
from datetime import date
from django.contrib import messages
#from constants.messages import errors,success
from constants.messages import errors,success

from django.utils.translation import gettext as _
from .services import productservice
from apps.purchases.models import shipping

from django.contrib.auth import login,authenticate,logout

from constants.messages import errors,success


_productService = productservice.ProductService()


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

	if currentUser.is_superuser:
		print("----------------------------")
		return redirect('store')
	else:
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
			message = errors.LOGIN_REQUIRED
			messages.success(request, message)
			return redirect('login')

	



