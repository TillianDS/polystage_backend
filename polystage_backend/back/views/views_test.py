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
    

from django.http import JsonResponse
from django.middleware.csrf import get_token

def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})