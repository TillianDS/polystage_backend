from rest_framework.permissions import BasePermission
from django.shortcuts import redirect
from django.urls import reverse_lazy

class RedirectUnauthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False
        else:
            login_url = reverse_lazy('login')  
            return redirect(login_url)
