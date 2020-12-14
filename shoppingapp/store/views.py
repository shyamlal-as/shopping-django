from django.shortcuts import render
from django.shortcuts import redirect
from .models import Categories,Product
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import productSerializer
from purchase.models import Purchases, ProductPurchases
from datetime import date
from shipping.models import shipping
from django.urls import resolve
# Create your views here.
pageno=1
pagenos=1
def store(request,page_num=1):
	global pageno
	pageno=1
	global pagenos
	products=Product.objects.get_queryset().order_by('id')
	product_paginator=Paginator(products,6)
	page_num=request.GET.get('page')
	if page_num is None:
		page=product_paginator.get_page(pagenos)
		print('dkkkkkkkkkkkkkkkk',pagenos)

	else:
		pagenos=page_num
		print('dkkkkkkkkkkkkkkkk',pagenos)
		page=product_paginator.get_page(pagenos)

	page=product_paginator.get_page(pagenos)
	context={
		'page':page,
	}
	return render(request,'store/store.html',context)
	#return store(request,pagenos)

def product(request,categories_id,page_num=1):
	global pagenos
	pagenos=1
	products=Product.objects.get_queryset().filter(categories_id=categories_id).order_by('id')
	product_paginator=Paginator(products,6)
	#page_number=request.GET.get('page')
	global pageno	
	page_num=request.GET.get('page')
	#print('dkkkkkkkkkkkkkkkk',pageno)
	if page_num is None:
		page=product_paginator.get_page(pageno)
		print('dkkkkkkkkkkkkkkkk',pageno)

	else:
		pageno=page_num
		print('dkkkkkkkkkkkkkkkk',pageno)
		page=product_paginator.get_page(pageno)

	context={
		'page':page,
		'cid':categories_id,
	}
	prod=request.POST.get('pid')

	return render(request,'store/prod.html',context)

def search(request):
	if request.method=='POST':
		search=request.POST['search']	
		products=Product.objects.all().filter(Q(name__icontains=search))
		product_paginator=Paginator(products,6)
		page_num=request.POST.get('page')
		page=product_paginator.get_page(page_num)
		context={
		'page':page,
		}
		
		return render(request,'store/store.html',context)
	else:
		return render(request,'store/store.html')


def searchProduct(request):
	if request.method=='POST':
		search=request.POST['search']	
		products=Product.objects.all().filter(Q(name__icontains=search))
		product_paginator=Paginator(products,6)
		page_num=request.POST.get('page')
		page=product_paginator.get_page(page_num)
		context={
		'page':page,
		}
		
		return redirect(request,'store/prod.html',context)
	else:
		return render(request,'store/prod.html')






def cart(request):
	try:
		prod=request.POST.get('pid')
		currentUser=request.user
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
				if not ProductPurchases.objects.filter(product_ID=prod,purchases_ID=n.id).exists():
					prod=request.POST.get('pid')
					pid=Product.objects.get(id=prod)
					pr=pid.price
					purchaseProduct=ProductPurchases(purchases_ID=Purchases.objects.latest('pk'),product_ID=pid,quantity=1,price=pr)
					purchaseProduct.save()
				else:
					pass			
			products=Product.objects.all().filter(categories_id=Product.objects.get(id=prod).categories_id)
		pag=request.POST.get('pag')
		page_num=request.GET.get('page')
		print('....The page you are looking for ...........',page_num)
		if(pag=='product'):
			global pageno
			print('The page NO =================',pageno)
			return product(request,Product.objects.get(id=prod).categories_id,pageno)
		elif(pag=='store'):
			global pagenos
			return store(request,pagenos)
	except:
		return render(request,'store/store.html')

def displayCart(request):
	global pagenos
	pagenos=1
	global pageno
	pageno=1
	currentUser=request.user
	eq=Purchases.objects.all().filter(Users_ID=currentUser.id,isActive=True).first()
	products=[]
	amount=0
	message=""
	try:
		if currentUser.is_authenticated:
			for each in ProductPurchases.objects.all().order_by('id'):
				if each.purchases_ID.id==eq.id and each.purchases_ID.isActive==True and each.purchases_ID.Users_ID==currentUser:
					print('results: ',each.purchases_ID.id)
					products.append(each)
					amount+=each.price*each.quantity
	except :
		print('-------------------Not Found-------------')
		message="Your Cart is empty"
	return render(request,'store/cart.html',{'products':products,'price':amount,'message':message})


def remove(request):
	idd=request.POST.get('idd')
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
	plus=request.POST.get('plus')
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
			

	return displayCart(request)
	#return render(request,'store/cart.html',{'products':products,'price':amount})



def minus(request):
	currentUser=request.user
	minus=request.POST.get('minus')
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
			
	return displayCart(request)

	#return render(request,'store/cart.html',{'products':products,'price':amount})

def complete(request):
	currentUser=request.user
	n=Purchases.objects.filter(Users_ID=currentUser,isActive=True).first()
	n.isActive=False
	n.save()
	address=request.POST.get('address')
	print(address)
	city=request.GET.POST('city')
	print(city)
	pincode=request.POST.get('pincode')
	print(pincode)
	shippingdets=shipping(Users_ID=request.user,address=address,city=city,pincode=pincode)
	shippingdets.save()
	return render(request,'store/complete.html')




def displayHistory(request):
	currentUser=request.user
	display=[]
	message=""

	for each in Purchases.objects.all().filter(Users_ID=currentUser,isActive=False):
		for eq in ProductPurchases.objects.filter(purchases_ID=each.id):
			display.append(eq)

	if len(display)==0:
		message="You have not made any purchases"
	return render(request,'store/cart2.html',{'products':display,'message':message})


def clearCart(request):
	currentUser=request.user
	purchase=request.POST.get('purchaseID')
	print("-----------------------------------------------------",purchase)
	Purchases.objects.all().filter(id=purchase).delete()

	return displayCart(request)

class productList(APIView):

	def get(self,request):
		product1=Product.objects.all()
		serializer=productSerializer(product1,many=True)
		return Response(serializer.data)
		