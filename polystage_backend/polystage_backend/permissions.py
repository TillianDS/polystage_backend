from rest_framework.permissions import BasePermission
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile == 'ADM'
    
class JuryPermission(BasePermission):
    def has_permission(self, request, view):
        ens = request.user.profile == 'ENS'
        pro = request.user.profile == 'PRO'
        return ens or pro
    
class EtuPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile == 'ETU'

class TuteurPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile == 'TUT'

class SuperUserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
    
class AdminJuryPermission(BasePermission):
    def has_permission(self, request, view):
        ens = request.user.profile == 'ENS'
        pro = request.user.profile == 'PRO'
        admin = request.user.profile == 'ADM'
        return ens or pro or admin
    
class TuteurPermission(BasePermission):
    def has_permission(self, request, view):
        tut = request.user.profile == 'TUT'
        return tut
    
