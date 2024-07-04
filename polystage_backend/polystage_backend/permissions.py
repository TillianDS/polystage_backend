from rest_framework.permissions import BasePermission
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import status


class RedirectUnauthenticated(BasePermission):
    def has_permission(self, request, view):
    
        return True
        
class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated