from rest_framework.response import Response
from rest_framework import status
from store.models import Product


class ResponseServices:

    def __init__(self,_message):
        self._message = _message


    def success(self):
        """
        API succesful
        :param self - instance of the class ResponseServices
        :return dictionary data: Contains success message, status code and status
        """
        data={'status':'success',
        'status-code':status.HTTP_200_OK,
        'message':self._message}
        return(data)

    def NotFound(self):
        """
        Unsuccesful API
        :param self - instance of the class ResponseServices
        :return dictionary data: Contains failure message, status code and status
        """
        data={'status':'failed',
        'status-code':status.HTTP_404_NOT_FOUND,
        'message':self._message}
        return(data)
