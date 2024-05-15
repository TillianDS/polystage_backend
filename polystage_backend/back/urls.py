"""from allauth.account.views import confirm_email"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import views_login, views_test, views_etudiant, views_users

urlpatterns = [
    path('test/', views_test.FiliereList.as_view()),
    path('test/<int:pk>/', views_test.filiere_details),

    #views_Users
    path('user/<int:pk>/', views_users.User_details.as_view()),
    path('enseignant/', views_users.EnseignantList.as_view()),
    path('adminlist/', views_users.AdminList.as_view()),
    path('professionnel/', views_users.ProfessionnelList.as_view()),
    path('tuteur/', views_users.TuteurList.as_view()),
    path('etudiant/', views_users.EtudiantList.as_view()),


    #views_login
    path('password/<int:pk>/', views_login.Change_password.as_view()),
    path('login/', views_login.CostumLogin.as_view()),


    ]

urlpatterns = format_suffix_patterns(urlpatterns)