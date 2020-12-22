
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from purchases.models import Purchases, ProductPurchases
from store.models import Product
from apps.store.services import ResponseServices
from api.v1.purchases.serializers import PurchaseSerializer, AddToCartSerializer, ConfirmPurchaseSerializer


#Create Cart
"""
@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def cart_api_view(request,slug):
    try:
        if not Purchases.objects.filter(Users_ID=currentUser.id,isActive=True).exists():  #Checking if added product already exists
                purchaseDetail=Purchases(Users_ID=request.user,date=date.today())           #Adding new purchase
                purchaseDetail.save()
                pid=Product.objects.get(id=prod)
                print("---------------------------Stock--------------------------",pid.stock)
                if pid.stock>0:
                    pr=pid.price
                #Adding and saving products to new purchase

                    purchaseProduct=ProductPurchases(purchases_ID=Purchases.objects.latest('pk'),product_ID=pid,quantity=1,price=pr)
                    purchaseProduct.save()
                    #pid.stock-=1
                    #pid.save()
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
                        #pid.stock-=1
                        #pid.save()

                else:
                    pass    
        obj=responseservices.ResponseServices(message)
        return Response(obj.success(), status=status.HTTP_200_OK)
    except:
        message='An unknown error has occured'
        obj=responseservices.ResponseServices(message)
        return Response(obj.NotFound(), status=status.HTTP_404_NOT_FOUND)


"""

# Purchase cart


@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def cart_purchase_api(request,slug):


    try:
        purchase = Purchases.objects.get(Users_ID=request.user, isActive=True)
    except Purchases.DoesNotExist:
        message='This user has no active cart'
        obj=responseservices.ResponseServices(message)
        return Response(obj.NotFound(), status.HTTP_404_NOT_FOUND)

    
    if request.method == "PUT":
        serializer = ConfirmPurchaseSerializer(purchase, data=request.data)
        if serializer.is_valid():
            serializer.save()
            message='Purchase Succesful'
        obj=responseservices.ResponseServices(message)
        return Response(obj.success(), status.HTTP_200_OK)

