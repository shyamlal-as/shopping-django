from purchases.models import Purchases, ProductPurchases
from store.models import Product, Categories
from purchases.models import shipping
from users.models import Profile
from datetime import date
from django.contrib import messages


class PurchaseServices:

    product=Product.objects
    category=Categories.objects
    purchase=Purchases.objects
    productPurchase=ProductPurchases.objects

    def CreateCart(self,request):
        prod=request.GET.get('pid')
        currentUser=request.user

        if not PurchaseServices.purchase.filter(Users_ID=currentUser.id,isActive=True).exists():
            purchaseDetail=Purchases(Users_ID=request.user,date=date.today())
            purchaseDetail.save()
            pid=PurchaseServices.product.get(id=prod)
            pr=pid.price
            purchaseProduct=ProductPurchases(purchases_ID=PurchaseServices.purchase.latest('pk'),product_ID=pid,quantity=1,price=pr)
            purchaseProduct.save()
        elif PurchaseServices.purchase.filter(Users_ID=currentUser.id,isActive=True).exists():
            print("---------------------Got in--------------")
            n=PurchaseServices.purchase.filter(Users_ID=currentUser,isActive=True).first()
            print("the needed one: ",n.id)
            if not PurchaseServices.productPurchase.filter(product_ID=prod,purchases_ID=n.id).exists():
                prod=request.GET.get('pid')
                print('prodd----------',prod)
                pid=PurchaseServices.product.get(id=prod)
                pr=pid.price
                purchaseProduct=ProductPurchases(purchases_ID=PurchaseServices.purchase.latest('pk'),product_ID=pid,quantity=1,price=pr)
                purchaseProduct.save()
            else:
                pass			
        products=PurchaseServices.product.all().filter(categories_id=PurchaseServices.product.get(id=prod).categories_id)


    def DisplayCart(self,request):
        currentUser=request.user
        eq=Purchases.objects.all().filter(Users_ID=currentUser.id,isActive=True).first()
        products=[]
        amount=0
        if PurchaseServices.purchase.filter(Users_ID=currentUser.id,isActive=True).exists():
            for each in PurchaseServices.productPurchase.all():
                if each.purchases_ID.id==eq.id and each.purchases_ID.isActive==True and each.purchases_ID.Users_ID==currentUser:
                    print('results: ',each.purchases_ID.id)
                    products.append(each)
                    amount+=each.price*each.quantity
        context = {'products':products,'price':amount}
        return(context)


    def RemoveProduct(self, request):
        idd=request.GET.get('idd')
        currentUser=request.user
        n=Purchases.objects.filter(Users_ID=currentUser,isActive=True).first()
        PurchaseServices.productPurchase.filter(product_ID=int(idd),purchases_ID=n.id).delete()
        amount=0
        eq=Purchases.objects.all().filter(Users_ID=currentUser.id,isActive=True).first()
        products=[]
        if currentUser.is_authenticated:
            for each in PurchaseServices.productPurchase.all():
                if each.purchases_ID.id==eq.id and each.purchases_ID.isActive==True and each.purchases_ID.Users_ID==currentUser:
                    print('results: ',each.purchases_ID.id)
                    products.append(each)
                    amount+=each.price*each.quantity
        context={'products':products,'price':amount}
        return(context)


    def IncreaseQuantity(self, request):
        currentUser=request.user
        plus=request.GET.get('plus')
        n=Purchases.objects.filter(Users_ID=currentUser,isActive=True).first()
        quantity=PurchaseServices.productPurchase.get(product_ID=int(plus),purchases_ID=n.id)
        newquantity=quantity.quantity+1
        quantity.quantity=newquantity
        quantity.save()
        amount =0
        eq=Purchases.objects.all().filter(Users_ID=currentUser.id,isActive=True).first()
        products=[]
        if currentUser.is_authenticated:
            for each in PurchaseServices.productPurchase.all():
                if each.purchases_ID.id==eq.id and each.purchases_ID.isActive==True and each.purchases_ID.Users_ID==currentUser:
                    print('results: ',each.purchases_ID.id)
                    products.append(each)
                    amount+=each.price*each.quantity
        context= {'products':products,'price':amount}
        return(context)


    
    def DecreaseQuantity(self, request):
        currentUser=request.user
        minus=request.GET.get('minus')
        n=Purchases.objects.filter(Users_ID=currentUser,isActive=True).first()
        quantity=PurchaseServices.productPurchase.get(product_ID=int(minus),purchases_ID=n.id)
        newquantity=quantity.quantity-1
        quantity.quantity=newquantity
        quantity.save()
        amount=0
        eq=Purchases.objects.all().filter(Users_ID=currentUser.id,isActive=True).first()
        products=[]
        if currentUser.is_authenticated:
            for each in PurchaseServices.productPurchase.all():
                if each.purchases_ID.id==eq.id and each.purchases_ID.isActive==True and each.purchases_ID.Users_ID==currentUser:
                    print('results: ',each.purchases_ID.id)
                    products.append(each)
                    amount+=each.price*each.quantity
        context ={'products':products,'price':amount}
        return(context)


    def Checkout(self, request):
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

    
    def ClearCart(self, request):
        currentUser=request.user
        purchase=request.GET.get('purchaseID')
        print("-----------------------------------------------------",purchase)
        Purchases.objects.all().filter(id=purchase).delete()