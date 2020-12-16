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
# Create your views here.

def store(request):
	#getting all products

	products=Product.objects.all()
	#Adding pagination

	product_paginator=Paginator(products,6)
	page_num=request.GET.get('page')
	page=product_paginator.get_page(page_num)
	context={
		'page':page,
	}
	return render(request,'store/store.html',context)



def checkout(request):
	context={}
	return render(request,'store/checkout.html',context)

def product(request,categories_id):
	#getting products of a category

	products=Product.objects.all().filter(categories_id=categories_id)
	
	#product_paginator=Paginator(products,6)
	#page_num=request.GET.get('page')
	#page=product_paginator.get_page(page_num)

	#request.session.get('cart').clear()
	context={
		#'page':page,
		'products':products
	}
	prod=request.POST.get('pid')

	return render(request,'store/prod.html',context)


def search(request):
	if request.method=='POST':
		#Getting search item

		search=request.POST['search']
		#filtering products to find search-item then displaying

		products=Product.objects.all().filter(Q(name__icontains=search))
		product_paginator=Paginator(products,6)
		page_num=request.GET.get('page')
		page=product_paginator.get_page(page_num)
		context={
		'page':page,
		'key':search,
		}
		
		return render(request,'store/search.html',context)
	else:
		return render(request,'store/store.html')



#Add to card feature
def cart(request):
	if request.user.is_authenticated:
		try:

			prod=request.GET.get('pid') #Getting product ID of selected Product
			currentUser=request.user    #Getting Current Active user

			if currentUser.is_authenticated:

				if not Purchases.objects.filter(Users_ID=currentUser.id,isActive=True).exists():  #Checking if added product already exists
					purchaseDetail=Purchases(Users_ID=request.user,date=date.today())			#Adding new purchase
					purchaseDetail.save()
					pid=Product.objects.get(id=prod)
					pr=pid.price
					#Adding and saving products to new purchase

					purchaseProduct=ProductPurchases(purchases_ID=Purchases.objects.latest('pk'),product_ID=pid,quantity=1,price=pr)
					purchaseProduct.save()

				#Checking for active carts corresponding to current user
				elif Purchases.objects.filter(Users_ID=currentUser.id,isActive=True).exists():
					n=Purchases.objects.filter(Users_ID=currentUser,isActive=True).first() #Finding active carts of current user
					if not ProductPurchases.objects.filter(product_ID=prod,purchases_ID=n.id).exists(): #Adding product to active cart
						prod=request.GET.get('pid')
						pid=Product.objects.get(id=prod)
						pr=pid.price
						#Saving the product to cart
						purchaseProduct=ProductPurchases(purchases_ID=Purchases.objects.latest('pk'),product_ID=pid,quantity=1,price=pr)
						purchaseProduct.save()
					else:
						pass			
				products=Product.objects.all().filter(categories_id=Product.objects.get(id=prod).categories_id)
			#return product(request,Product.objects.get(id=prod).categories_id)
			messages.success(request,  'added To Cart.')
			return redirect(request.META['HTTP_REFERER'])
			
		except:
			return render(request,'store/cart.html')
	
	else:
		messages.success(request,  'added To Cart.')
		return redirect('login')



	
#Displaying products added to cart
def displayCart(request):
	if request.user.is_authenticated:
		currentUser=request.user
		eq=Purchases.objects.all().filter(Users_ID=currentUser.id,isActive=True).first()
		products=[]
		amount=0
		try:
			if currentUser.is_authenticated:
				for each in ProductPurchases.objects.all().order_by('product_ID'):
					if each.purchases_ID.id==eq.id and each.purchases_ID.isActive==True and each.purchases_ID.Users_ID==currentUser:
						print('results: ',each.purchases_ID.id)
						products.append(each)
						amount+=each.price*each.quantity
		except :
			print('-------------------Not Found-------------')
		
				

		return render(request,'store/cart.html',{'products':products,'price':amount})
	else:
		return redirect('login')


#removing product added to cart
def remove(request):
	idd=request.GET.get('idd')
	currentUser=request.user
	n=Purchases.objects.filter(Users_ID=currentUser,isActive=True).first()
	ProductPurchases.objects.filter(product_ID=int(idd),purchases_ID=n.id).delete()
	amount=0
	eq=Purchases.objects.all().filter(Users_ID=currentUser.id,isActive=True).first()
	products=[]
	if currentUser.is_authenticated:
		for each in ProductPurchases.objects.all():
			if each.purchases_ID.id==eq.id and each.purchases_ID.isActive==True and each.purchases_ID.Users_ID==currentUser:
				print('results: ',each.purchases_ID.id)
				products.append(each)
				amount+=each.price*each.quantity
			
	return render(request,'store/cart.html',{'products':products,'price':amount})




#Addition of product quantity
def plus(request):
	currentUser=request.user 	#Getting currently active user
	plus=request.GET.get('plus') #Getting product ID of product to be incremented in quantity
	n=Purchases.objects.filter(Users_ID=currentUser,isActive=True).first()  #Getting user's active carts
	quantity=ProductPurchases.objects.get(product_ID=int(plus),purchases_ID=n.id) #Getting product from active cart and decrementing quantity and saving
	newquantity=quantity.quantity+1
	quantity.quantity=newquantity
	quantity.save()
	amount =0
	eq=Purchases.objects.all().filter(Users_ID=currentUser.id,isActive=True).first()
	products=[]
	if currentUser.is_authenticated:
		for each in ProductPurchases.objects.all().order_by('id'):
			if each.purchases_ID.id==eq.id and each.purchases_ID.isActive==True and each.purchases_ID.Users_ID==currentUser:
				print('results: ',each.purchases_ID.id)
				products.append(each)
				amount+=each.price*each.quantity
			

	return render(request,'store/cart.html',{'products':products,'price':amount})



def minus(request):
	currentUser=request.user
	minus=request.GET.get('minus')
	n=Purchases.objects.filter(Users_ID=currentUser,isActive=True).first()
	quantity=ProductPurchases.objects.get(product_ID=int(minus),purchases_ID=n.id)
	newquantity=quantity.quantity-1
	quantity.quantity=newquantity
	quantity.save()
	amount=0
	eq=Purchases.objects.all().filter(Users_ID=currentUser.id,isActive=True).first()
	products=[]
	if currentUser.is_authenticated:
		for each in ProductPurchases.objects.all().order_by('id'):
			if each.purchases_ID.id==eq.id and each.purchases_ID.isActive==True and each.purchases_ID.Users_ID==currentUser:
				print('results: ',each.purchases_ID.id)
				products.append(each)
				amount+=each.price*each.quantity
			

	return render(request,'store/cart.html',{'products':products,'price':amount})


#Completing cart purchase
def complete(request):
	currentUser=request.user
	n=Purchases.objects.filter(Users_ID=currentUser,isActive=True).first()
	n.isActive=False
	n.save()
	address=request.GET.get('address')
	print(address)
	city=request.GET.get('city')
	print(city)
	pincode=request.GET.get('pincode')
	print(pincode)
	shippingdets=shipping(Users_ID=request.user,address=address,city=city,pincode=pincode)
	shippingdets.save()
	return render(request,'store/complete.html')



#Product details
def details(request,slug):
	product=Product.objects.filter(id=slug)
	context={
		'product':product
	}
	return render(request, 'store/details.html', context)



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
		return redirect('login')




def clearCart(request):
	currentUser=request.user
	purchase=request.GET.get('purchaseID')
	print("-----------------------------------------------------",purchase)
	Purchases.objects.all().filter(id=purchase).delete()

	return displayCart(request)
