from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from ..serializers import UserSerializer

class user_cas(APIView):
    def get(self, request, format = None):
        user = request.user
        return Response(UserSerializer(user).data)