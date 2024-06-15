from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
     #views_Users
    path('mailOpenPolystage/', views.sendMailOpenPolystage.as_view()),
    
    path('confirmationForm/', views.confirmationForm.as_view()),
    path('modificationForm/', views.modificationForm.as_view()),

    ]

urlpatterns = format_suffix_patterns(urlpatterns)