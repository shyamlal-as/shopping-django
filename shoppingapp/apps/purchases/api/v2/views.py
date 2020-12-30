from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from apps.purchases.models import Purchases, ProductPurchases
from apps.store.models import Product


from .serializers import PurchaseSerializer, AddToCartSerializer, ConfirmPurchaseSerializer


#Create Cart

@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def cart_api_view(request,slug):
    try:
        if not Purchases.objects.filter(Users_ID=request.user,isActive=True).exists():
            purchaseDetail=Purchases(Users_ID=request.user)
            purchaseDetail.save()
            pid=Product.objects.get(id=slug)
            pr=pid.price
            purchaseProduct=ProductPurchases(purchases_ID=Purchases.objects.latest('pk'),product_ID=pid,quantity=1,price=pr)
            purchaseProduct.save()
        else:
            purchase=Purchases.objects.get(Users_ID=request.user,isActive=True)
            #print("the needed one: ",n.id)
            if not ProductPurchases.objects.filter(product_ID=slug,purchases_ID=purchase.id).exists():
                #prod=request.GET.get('pid')
                product=Product.objects.get(id=slug)
                pr=product.price
                pid=Product.objects.get(id=slug)
                purchaseProduct=ProductPurchases(purchases_ID=purchase,product_ID=pid,quantity=1,price=pr)
                purchaseProduct.save()
            else:
                purchaseProduct=ProductPurchases.objects.get(product_ID=slug,purchases_ID=purchase.id)
                print(purchaseProduct)
                print(purchaseProduct.quantity)
                purchaseProduct.quantity=purchaseProduct.quantity+1
                print(purchaseProduct.quantity)
                purchaseProduct.save()

			
            #products=Product.objects.all().filter(categories_id=Product.objects.get(id=prod).categories_id)
        #return product(request,Product.objects.get(id=prod).categories_id)
        #messages.success(request,  'added To Cart.')
        data={}
        data['message']='success'
        return Response(data, status=status.HTTP_200_OK)
    except:
        data={}
        data['message']='Cart Not created'
        return Response(data, status=status.HTTP_404_NOT_FOUND)



    """

    purchases = Purchases(Users_ID= request.user)
    

    if request.method == 'POST':
        serializer = PurchaseSerializer(purchases, data=request.data)
        data ={}
        if serializer.is_valid():
            user = serializer.save()
            propurchasefn(request,slug)
            data={'message':'Cart Created'}
            return Response(data)


def propurchasefn(request,slug):
    product = Product.objects.filter(id=slug).first()
    propurchases = ProductPurchases(purchases_ID= Purchases.objects.latest('pk'), 
    product_ID=product,
    price=product.price,quantity=1)
    serializer = AddToCartSerializer(propurchases, data=request.data)
    data={}
    if serializer.is_valid():
        user=serializer.save()
        data['purch']=' success'
        return Response(data)

"""

# Purchase cart


@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def cart_purchase_api(request,slug):


    try:
        purchase = Purchases.objects.get(Users_ID=request.user, isActive=True)
    except Purchases.DoesNotExist:
        data={}
        data['message']='No product on this id'
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    
    if request.method == "PUT":
        #propurchases = purchase(isActive=False, Users_ID=request.user)
        #dat['isActive']=False
        serializer = ConfirmPurchaseSerializer(purchase, data=request.data)
        print('----------------------------------------')
        print(request.data)
        print('------------------------------')
        data={}
        if serializer.is_valid():
            serializer.save()
            data['success']='Update Succesful'
            return Response(data=data)
        return Response(serializer.errors, status.HTTP_200_OK)


# Nothing


@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def cart_purchase_api(request,slug):


    try:
        purchase = Purchases.objects.get(Users_ID=request.user, isActive=True)
    except Purchases.DoesNotExist:
        data={}
        data['message']='No product on this id'
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    
    if request.method == "PUT":
        #propurchases = purchase(isActive=False, Users_ID=request.user)
        dat={}
        #dat['isActive']=False
        serializer = ConfirmPurchaseSerializer(purchase, data=request.data)
        print('----------------------------------------')
        print(request.data)
        print('------------------------------')
        data={}
        if serializer.is_valid():
            serializer.save()
            data['success']='Update Succesful'
            return Response(data=data)
        return Response(serializer.errors, status.HTTP_200_OK)