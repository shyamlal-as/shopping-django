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

def cart(request):
	prod=request.POST.get('pid')
	currentUser=request.user
	if currentUser.is_authenticated:
		if not ProductPurchases.objects.filter(product_ID=prod).exists():
			purchaseDetail=Purchases(Users_ID=request.user,date=date.today())
			purchaseDetail.save()
			pid=Product.objects.get(id=prod)
			pr=pid.price
			purchaseProduct=ProductPurchases(purchases_ID=Purchases.objects.latest('pk'),product_ID=pid,quantity=1,price=pr)
			purchaseProduct.save()
	products=Product.objects.all().filter(categories_id=pid.categories_id)
	return render(request,'store/prod.html',{'products':products})


def displayCart(request):
	productIDs=[]
	prodIns=[]
	amount=0
	for each in ProductPurchases.objects.all():
		#if Product.objects.filter(id=each.product_ID).exists():
		productIDs.append(each.product_ID)

	for each in productIDs:
		prodIns.append(Product.objects.get(id=each.id))

	for each in prodIns:
		amount+=each.price



	return render(request,'store/cart.html',{'products':prodIns,'price':amount})

class productList(APIView):

	def get(self,request):
		product1=Product.objects.all()
		serializer=productSerializer(product1,many=True)
		return Response(serializer.data)
		