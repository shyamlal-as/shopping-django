from rest_framework.response import Response
from rest_framework import status
from store.models import Product
from constants.messages import success, errors

class ResponseServices:

    def __init__(self,_message):
        self._message = _message


    def success(self):
        data={'status':success.SUCCESS,
        'status-code':status.HTTP_200_OK,
        'message':self._message}
        return(data)

    def NotFound(self):
        data={'status':errors.FAILED,
        'status-code':status.HTTP_404_NOT_FOUND,
        'message':self._message}
        return(data)


