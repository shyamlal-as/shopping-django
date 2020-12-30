from rest_framework.response import Response
from rest_framework import status
from constants.messages import success, errors

class ResponseService:

    def __init__(self,_message):

        """
        Set value to message tag on initialisation of class

        :param string message: Message to return to user

        :return null: 
        """

        self._message = _message


    def success(self):

        """
        Return message with status code 200

        :param null :

        :return Dictionary: Dictionary with the response messages
        """

        data={'status':success.SUCCESS,
        'status-code':status.HTTP_200_OK,
        'message':self._message}
        return(data)

    def NotFound(self):

        """
        Return message with status code 404

        :param null :

        :return Dictionary: Dictionary with the response messages
        """

        data={'status':errors.FAILED,
        'status-code':status.HTTP_404_NOT_FOUND,
        'message':self._message}
        return(data)


