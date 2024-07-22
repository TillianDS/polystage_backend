from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
     #views_Users
    path('openSession/<int:pk>/', views.OpenSession.as_view()),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)