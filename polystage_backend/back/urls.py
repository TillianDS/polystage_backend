"""from allauth.account.views import confirm_email"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import views_login, views_test, views_etudiant, views_users, views_admin, views_promo_filiere

urlpatterns = [
    path('test/', views_test.FiliereList.as_view()),
    path('test/<int:pk>/', views_test.filiere_details),

    #views_Users
    path('userDetails/<int:pk>/', views_users.UserDetails.as_view()),
    path('userList/<str:profile>/', views_users.UserList.as_view()),

    #views_login
    path('changePassword/<int:pk>/', views_login.ChangePassword.as_view()),
    path('login/', views_login.CostumLogin.as_view()),
    path('codeReset/', views_login.SendCodeEmail.as_view()),
    path('code/', views_login.gestionCode.as_view()),

    #views_admin
    path('userSearch/', views_admin.GetUser.as_view()),

    #views_promo_filiere
    path('promoDetails/<int:pk>/', views_promo_filiere.PromoDetails.as_view()),
    path('promoList/', views_promo_filiere.PromoList.as_view()),

    path('filiereList/', views_promo_filiere.FiliereList.as_view()),
    path('filiereDetails/<int:pk>/', views_promo_filiere.FiliereDetails.as_view()),

    path('promoFiliere/', views_promo_filiere.PromoFiliere.as_view()),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)