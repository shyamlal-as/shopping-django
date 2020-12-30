from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from apps.purchases.models import Purchases, ProductPurchases
from apps.store.models import Product

from apps.purchases.services import purchaseservice
from apps.purchases.services import responseservice
from .serializers import PurchaseSerializer, AddToCartSerializer, ConfirmPurchaseSerializer

_purchaseService = purchaseservice.PurchaseService()


#Create Cart

@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def cart_api_view(request,slug):

    """
    Create a cart

    :param WSGI Request request: Request object
    :param slug slug: Product id

    :return Response: Success or failure message
    """

    try:
        message=_purchaseService.CreateCart(request,slug)
        obj=responseservice.ResponseService(message)
        return Response(obj.success(), status=status.HTTP_200_OK)
    except:
        message='An unknown error has occured'
        obj=responseservice.ResponseService(message)
        return Response(obj.NotFound(), status=status.HTTP_404_NOT_FOUND)




# Purchase cart


@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def cart_purchase_api(request,slug):

    """
    Checkout the current cart

    :param WSGI Request request: Request object
    :param slug slug: Product id

    :return Response: Success or failure message
    """

    try:
        purchase = Purchases.objects.get(Users_ID=request.user, isActive=True)
    except Purchases.DoesNotExist:
        message='This user has no active cart'
        obj=responseservice.ResponseService(message)
        return Response(obj.NotFound(), status.HTTP_404_NOT_FOUND)

    
    if request.method == "PUT":
        serializer = ConfirmPurchaseSerializer(purchase, data=request.data)
        if serializer.is_valid():
            serializer.save()
            message='Purchase Succesful'
        obj=responseservice.ResponseService(message)
        return Response(obj.success(), status.HTTP_200_OK)

