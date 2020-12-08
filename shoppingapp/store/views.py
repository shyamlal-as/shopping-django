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
	pid=request.POST.get('pid')

	cart = request.session.get('cart')

	if cart:
		quantity=cart.get(pid)
		if quantity:
			#print('quantity')
			cart[pid]=quantity+1	
		else:
			cart[pid]=1
	else:
		cart={}
		cart[pid]=1
	request.session['cart']=cart
	#for k, v in dict(cart).items():
	#	if v is None:
	 #   	del cart[k]
	"""for k, v in cart.items():
		if isinstance(v, dict):
			nested = cleanNullTerms(v)
		if len(nested.keys()) > 0:
			clean[k] = nested
	  elif v is not None:
	  	clean[k] = v
	cart=clean"""

	print('cart',request.session['cart'])
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


class productList(APIView):

	def get(self,request):
		product1=Product.objects.all()
		serializer=productSerializer(product1,many=True)
		return Response(serializer.data)
		