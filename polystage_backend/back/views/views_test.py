from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import *
from ..serializers import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class test(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None ):
        user = request.user
        return Response({"message": UserSerializer(user).data})