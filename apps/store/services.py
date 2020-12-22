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


class display():


	def storeDisplay(request,products):
		#products=Product.objects.all()
		product_paginator=Paginator(products,3)
		page_num=request.GET.get('page')
		page=product_paginator.get_page(page_num)
		return page

	

class searching():

	def search(request,item):
		#filtering products to find search-item then displaying

		products=Product.objects.all().filter(Q(name__icontains=item))
		
		#return products
		page=display.storeDisplay(request,products)

		return page


class cartop():

	def addToCart(request,prod):

		currentUser=request.user    #Getting Current Active user

		if currentUser.is_authenticated:

			if not Purchases.objects.filter(Users_ID=currentUser.id,isActive=True).exists():  #Checking if added product already exists
				purchaseDetail=Purchases(Users_ID=request.user,date=date.today())			#Adding new purchase
				purchaseDetail.save()
				pid=Product.objects.get(id=prod)
				print("---------------------------Stock--------------------------",pid.stock)
				if pid.stock>0:
					pr=pid.price
				#Adding and saving products to new purchase

					purchaseProduct=ProductPurchases(purchases_ID=Purchases.objects.latest('pk'),product_ID=pid,quantity=1,price=pr)
					purchaseProduct.save()
					pid.stock-=1
					pid.save()
			#Checking for active carts corresponding to current user
			elif Purchases.objects.filter(Users_ID=currentUser.id,isActive=True).exists():
				n=Purchases.objects.filter(Users_ID=currentUser,isActive=True).first() #Finding active carts of current user
				if not ProductPurchases.objects.filter(product_ID=prod,purchases_ID=n.id).exists(): #Adding product to active cart
					prod=request.GET.get('pid')
					pid=Product.objects.get(id=prod)
					if pid.stock>0:
						pr=pid.price
					#Saving the product to cart
						purchaseProduct=ProductPurchases(purchases_ID=Purchases.objects.latest('pk'),product_ID=pid,quantity=1,price=pr)
						purchaseProduct.save()
						pid.stock-=1
						pid.save()

				else:
					pass			
			products=Product.objects.all().filter(categories_id=Product.objects.get(id=prod).categories_id)


		return True


	def displayCart(request):
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
						
				return products,amount
		except :
			print('-------------------Not Found-------------')	


	def remove(request,idd):
		currentUser=request.user
		prod=Product.objects.get(id=idd)
		n=Purchases.objects.filter(Users_ID=currentUser,isActive=True).first()
		quantity=ProductPurchases.objects.get(product_ID=int(idd),purchases_ID=n.id)
		prod.stock+=quantity.quantity
		prod.save()
		ProductPurchases.objects.filter(product_ID=int(idd),purchases_ID=n.id).delete()



	def plus(request,idd):

		currentUser=request.user 	#Getting currently active user
		prod=Product.objects.get(id=idd)
		n=Purchases.objects.filter(Users_ID=currentUser,isActive=True).first()  #Getting user's active carts
		quantity=ProductPurchases.objects.get(product_ID=int(idd),purchases_ID=n.id) #Getting product from active cart and incrementing quantity and saving
		if prod.stock>0:
			newquantity=quantity.quantity+1
			quantity.quantity=newquantity
			quantity.save()
			prod.stock-=1;
			prod.save()

	def minus(request,idd):

		currentUser=request.user 	#Getting currently active user
		prod=Product.objects.get(id=idd)
		n=Purchases.objects.filter(Users_ID=currentUser,isActive=True).first()  #Getting user's active carts
		quantity=ProductPurchases.objects.get(product_ID=int(idd),purchases_ID=n.id) #Getting product from active cart and decrementing quantity and saving
		if quantity.quantity>1:
			newquantity=quantity.quantity-1
			quantity.quantity=newquantity
			quantity.save()
			prod.stock+=1;
			prod.save()	
		elif quantity.quantity==1:
			cartop.remove(request,idd)	


	def checkout(request):
		currentUser=request.user
		n=Purchases.objects.filter(Users_ID=currentUser,isActive=True).first()
		n.isActive=False
		n.save()
		address=request.GET.get('address')
		city=request.GET.get('city')
		pincode=request.GET.get('pincode')
		shippingdets=shipping(Users_ID=request.user,address=address,city=city,pincode=pincode)
		shippingdets.save()