from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from store.models import Product
from store.api.serializers import ProductSerializer


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_detail_product_view(request,slug):

    try:
        product= Product.objects.get(id=slug)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    
    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)