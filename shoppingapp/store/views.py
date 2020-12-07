from django.shortcuts import render

from .models import Categories,Product
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator

from django.shortcuts import get_object_or_404

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
	product_paginator=Paginator(products,6)
	page_num=request.GET.get('page')
	page=product_paginator.get_page(page_num)
	context={
		'page':page,
	}
	return render(request,'store/prod.html',context)


def details(request,slug):
	product=Product.objects.filter(id=slug)
	context={
		'product':product
	}
	return render(request, 'store/details.html', context)



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
		'key':search
		}
		
		return render(request,'store/search.html',context)
	else:
		return render(request,'store/search.html')

