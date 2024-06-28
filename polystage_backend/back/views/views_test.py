from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import *
from ..serializers import *
from rest_framework import status

class test(APIView):
    def get(self, request, format=None ):
        users = CustomUser.objects.filter(profile = "profile")
        for user in users:
            user.hard_delete()
        return Response({"delete": "delete"})