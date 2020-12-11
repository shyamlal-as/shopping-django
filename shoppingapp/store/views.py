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
	products=Product.objects.all()
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

def category(request):
	lists=Categories.objects.all()
	return render(request,'store/first.html',{'lists':lists})

def search(request):
	if request.method=='POST':
		search=request.POST['search']	
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






def minus(request):
	minus=request.POST.get('minus')	
	pid=ProductPurchases.objects.get(product_ID=int(minus))
	newquantity=pid.quantity-1
	pid.quantity=newquantity
	product=[]

	pid.save()

	productIDs=[]
	prodIns=[]
	amount=0
	for each in ProductPurchases.objects.all():
		productIDs.append(each.product_ID)

	for each in productIDs:
		prodIns.append(Product.objects.get(id=each.id))
		amount+=each.price
		product.append(ProductPurchases.objects.get(product_ID=each.id))
		

	return render(request,'store/cart.html',{'products':product,'price':amount})




def cart(request):
	if request.user.is_authenticated:
		try:
			prod=request.GET.get('pid')
			print("What it should be -------",prod)
			currentUser=request.user
			print('user',currentUser)
			if currentUser.is_authenticated:

				if not Purchases.objects.filter(Users_ID=currentUser.id,isActive=True).exists():
					purchaseDetail=Purchases(Users_ID=request.user,date=date.today())
					purchaseDetail.save()
					pid=Product.objects.get(id=prod)
					pr=pid.price
					purchaseProduct=ProductPurchases(purchases_ID=Purchases.objects.latest('pk'),product_ID=pid,quantity=1,price=pr)
					purchaseProduct.save()
				elif Purchases.objects.filter(Users_ID=currentUser.id,isActive=True).exists():
					print("---------------------Got in--------------")
					n=Purchases.objects.filter(Users_ID=currentUser,isActive=True).first()
					print("the needed one: ",n.id)
					if not ProductPurchases.objects.filter(product_ID=prod,purchases_ID=n.id).exists():
						prod=request.GET.get('pid')
						print('prodd----------',prod)
						pid=Product.objects.get(id=prod)
						pr=pid.price
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



	

def displayCart(request):
	if request.user.is_authenticated:
		currentUser=request.user
		eq=Purchases.objects.all().filter(Users_ID=currentUser.id,isActive=True).first()
		products=[]
		amount=0
		try:
			if currentUser.is_authenticated:
				for each in ProductPurchases.objects.all():
					if each.purchases_ID.id==eq.id and each.purchases_ID.isActive==True and each.purchases_ID.Users_ID==currentUser:
						print('results: ',each.purchases_ID.id)
						products.append(each)
						amount+=each.price*each.quantity
		except :
			print('-------------------Not Found-------------')
		
				

		return render(request,'store/cart.html',{'products':products,'price':amount})
	else:
		return redirect('login')



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





def plus(request):
	currentUser=request.user
	plus=request.GET.get('plus')
	n=Purchases.objects.filter(Users_ID=currentUser,isActive=True).first()
	quantity=ProductPurchases.objects.get(product_ID=int(plus),purchases_ID=n.id)
	newquantity=quantity.quantity+1
	quantity.quantity=newquantity
	quantity.save()
	amount =0
	eq=Purchases.objects.all().filter(Users_ID=currentUser.id,isActive=True).first()
	products=[]
	if currentUser.is_authenticated:
		for each in ProductPurchases.objects.all():
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
		for each in ProductPurchases.objects.all():
			if each.purchases_ID.id==eq.id and each.purchases_ID.isActive==True and each.purchases_ID.Users_ID==currentUser:
				print('results: ',each.purchases_ID.id)
				products.append(each)
				amount+=each.price*each.quantity
			

	return render(request,'store/cart.html',{'products':products,'price':amount})

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
