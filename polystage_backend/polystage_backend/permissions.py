from rest_framework.permissions import BasePermission
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import status
class RedirectUnauthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        else:
            print("ici")
            login_url = reverse('login') 
            return Response({"detail": "Vous devez être connecté pour accéder à cette ressource."}, status=status.HTTP_403_FORBIDDEN)                    
class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated