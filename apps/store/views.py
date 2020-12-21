from django.shortcuts import render, redirect
from .models import Categories,Product
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from purchases.models import Purchases, ProductPurchases
from users.models import Profile
from datetime import date
from django.contrib import messages

from purchases.models import shipping
from django.utils.translation import ugettext_lazy as _


from .services import display,searching,cartop


# Create your views here.

def store(request):
	"""
	Display of homepage

	:param Request request: Request

	:return HTML: store.html - homepage
	"""

	products=Product.objects.all()
	page=display.storeDisplay(request,products)
	context={
		'page':page,
		}
	
	return render(request,'store/store.html',context)



def product(request,categories_id):
	"""
	Categorical display of products

	:param Request request: Request
	:param int categories_id: ID of the corresponding category

	:return HTML: prod.html - categorical view
	"""

	#getting products of a category
	products=Product.objects.filter(categories_id=categories_id)
	page=display.storeDisplay(request,products)

	context={
		'page':page,
		}

	return render(request,'store/prod.html',context)


def search(request):
	"""
	Searching products by name 

	:param Request request: Request

	:return HTML: search.html - display products matching search
	"""

	if request.method=='POST':
		#Getting search item

		item=request.POST['search']
		page=searching.search(request,item)
		
		context={
		'page':page,
		'key':item,
		}
		
		return render(request,'store/search.html',context)
	else:
		return render(request,'store/search.html')



#Add to card feature
def cart(request):
	"""
	Adding product to cart 

	:param Request request: Request

	:return redirect : redirected to the same page
	:return redirect login : redirected to login page for unauthenticated user
	"""

	if request.user.is_authenticated:
		try:

			prod=request.GET.get('pid') #Getting product ID of selected Product

			value=cartop.addToCart(request,prod)

			messages.success(request,  'added To Cart.')
			return redirect(request.META['HTTP_REFERER'])
			
		except:
			return render(request,'store/cart.html')
	
	else:
		messages.success(request,  'added To Cart.')
		return redirect('login')



	
#Displaying products added to cart
def displayCart(request):
	"""
	Displaying products in cart 

	:param Request request: Request

	:return HTML: cart.html - displaying the cart
	"""

	if request.user.is_authenticated:

		products,amount=cartop.displayCart(request)		

		return render(request,'store/cart.html',{'products':products,'price':amount})
	else:
		return redirect('login')


#removing product added to cart
def remove(request):
	"""
	Removing product from cart 

	:param Request request: Request

	:return view: displayCart - displaying the cart
	"""

	idd=request.GET.get('idd')
	cartop.remove(request,idd)
	return displayCart(request)		
	




#Addition of product quantity
def plus(request):
	"""
	Incrementing product quantity 

	:param Request request: Request

	:return view: displayCart - displaying the cart
	"""

	idd=request.GET.get('plus') #Getting product ID of product to be incremented in quantity
	cartop.plus(request,idd)
	return displayCart(request)


def minus(request):
	"""
	Decrementing product quantity 

	:param Request request: Request

	:return view: displayCart - displaying the cart
	"""


	idd=request.GET.get('minus') #Getting product ID of product to be incremented in quantity
	cartop.minus(request,idd)
	return displayCart(request)



#Completing cart purchase
def complete(request):
	"""
	Completing the purchase 

	:param Request request: Request

	:return HTML: complete.html - Page denoting purchase-completed
	"""


	cartop.checkout(request)
	return render(request,'store/complete.html')



#Product details
def details(request,slug):
	"""
	Displaying product detail 

	:param Request request: Request

	:return HTML: details.html - product detail page
	"""


	product=Product.objects.filter(id=slug)
	context={
		'product':product
	}
	return render(request, 'store/details.html', context)



def profile(request):
	"""
	Displaying user's profile 

	:param Request request: Request

	:return HTML: profile.html - user profile page
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
		return redirect('login')




def clearCart(request):
	"""
	Emptying the cart 

	:param Request request: Request

	:return view: displayCart - displaying the cart
	"""

	currentUser=request.user
	purchase=request.GET.get('purchaseID')
	print("-----------------------------------------------------",purchase)
	Purchases.objects.all().filter(id=purchase).delete()

	return displayCart(request)
