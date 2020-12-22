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

    def CreateCart(self,request,slug):

        if not PurchaseServices().purchase.filter(Users_ID=request.user,isActive=True).exists():
            purchaseDetail=Purchases(Users_ID=request.user)
            purchaseDetail.save()
            pid=PurchaseServices().product.get(id=slug)
            pr=pid.price
            purchaseProduct=ProductPurchases(purchases_ID=PurchaseServices().purchase.latest('pk'),product_ID=pid,quantity=1,price=pr)
            purchaseProduct.save()
            message='A cart has been created'
        else:
            purchase=PurchaseServices().purchase.get(Users_ID=request.user,isActive=True)
            if not PurchaseServices().productPurchase.filter(product_ID=slug,purchases_ID=purchase.id).exists():
                product=PurchaseServices().product.get(id=slug)
                pr=product.price
                pid=PurchaseServices().product.get(id=slug)
                purchaseProduct=ProductPurchases(purchases_ID=purchase,product_ID=pid,quantity=1,price=pr)
                purchaseProduct.save()
                message='Product was added to the cart'
            else:
                purchaseProduct=PurchaseServices().productPurchase.get(product_ID=slug,purchases_ID=purchase.id)
                purchaseProduct.quantity=purchaseProduct.quantity+1
                purchaseProduct.save()
                message='Quantity of the product increased by one'
        return(message)
                
                
    def DisplayCart(self,request):
        eq=PurchaseServices().purchase.filter(Users_ID=request.user,isActive=True).first()
        products=[]
        amount=0
        if PurchaseServices.purchase.filter(Users_ID=request.user,isActive=True).exists():
            for each in PurchaseServices.productPurchase.order_by('product_ID'):
                if each.purchases_ID.id==eq.id and each.purchases_ID.isActive==True and each.purchases_ID.Users_ID==request.user:
                    products.append(each)
                    amount+=each.price*each.quantity
        context = {'products':products,'price':amount}
        return(context)


    def RemoveProduct(self, request):
        idd=request.POST.get('id')
        n=PurchaseServices().purchase.filter(Users_ID=request.user,isActive=True).first()
        PurchaseServices.productPurchase.filter(product_ID=int(idd),purchases_ID=n.id).delete()
        context=PurchaseServices().DisplayCart(request)
        return(context)


    def IncreaseQuantity(self, request):
        
        plus=request.POST.get('id')
        n=PurchaseServices().purchase.filter(Users_ID=request.user,isActive=True).first()
        quantity=PurchaseServices.productPurchase.get(product_ID=int(plus),purchases_ID=n.id)
        prod=Product.objects.get(id=plus)
        if quantity.quantity<prod.stock:
            newquantity=quantity.quantity+1
            quantity.quantity=newquantity
            quantity.save()
        context=PurchaseServices().DisplayCart(request)
        return(context)


    
    def DecreaseQuantity(self, request):
        
        minus=request.POST.get('id')
        n=PurchaseServices.purchase.filter(Users_ID=request.user,isActive=True).first()
        quantity=PurchaseServices.productPurchase.get(product_ID=int(minus),purchases_ID=n.id)
        if(quantity.quantity == 1):
            PurchaseServices().RemoveProduct(request)
        else:
            newquantity=quantity.quantity-1
            quantity.quantity=newquantity
            quantity.save()
        context=PurchaseServices().DisplayCart(request)
        return(context)


    def Checkout(self, request):
        success=1
        currentUser=request.user
        n=Purchases.objects.filter(Users_ID=currentUser,isActive=True).first()
        for each in ProductPurchases.objects.filter(purchases_ID=n.id):
            if each.quantity<=each.product_ID.stock:
                q=each.quantity
                each.product_ID.stock-=q
                each.product_ID.save()
            else:
                success=0
                break
        if success==1:
            n.isActive=False
            n.save()
            address=request.GET.get('address')
            city=request.GET.get('city')
            pincode=request.GET.get('pincode')
            shippingdets=shipping(Users_ID=request.user,address=address,city=city,pincode=pincode)
            shippingdets.save()
            return 1
        else:
            print("---------------------------------------Unsuccesfull-------------------")
            for each in ProductPurchases.objects.filter(purchases_ID=n.id):
                if each.quantity>each.product_ID.stock:
                    diff=each.quantity-each.product_ID.stock
                    for i in range(int(diff)):
                        cartop.minus(request,each.product_ID.id)			
            return 0

    
    def ClearCart(self, request):
        
        purchase=request.GET.get('purchaseID')
        PurchaseServices().purchase.filter(id=purchase).delete()