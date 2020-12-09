from django.shortcuts import render
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

def cart(request):
	print('Cart')
	context={}
	return render(request,'store/cart.html',context)

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
		}
		
		return render(request,'store/store.html',context)
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
	return render(request,'store/prod.html',{'products':products})

def displayCart(request):
	currentUser=request.user
	eq=Purchases.objects.all().filter(Users_ID=currentUser.id,isActive=True).first()
	products=[]
	amount=0
	if currentUser.is_authenticated:
		for each in ProductPurchases.objects.all():
			if each.purchases_ID.id==eq.id and each.purchases_ID.isActive==True and each.purchases_ID.Users_ID==currentUser:
				print('results: ',each.purchases_ID.id)
				products.append(each)
				amount+=each.price*each.quantity
			

	return render(request,'store/cart.html',{'products':products,'price':amount})



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

	return render(request,'store/complete.html')

class productList(APIView):

	def get(self,request):
		product1=Product.objects.all()
		serializer=productSerializer(product1,many=True)
		return Response(serializer.data)
		