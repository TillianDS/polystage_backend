"""from allauth.account.views import confirm_email"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import views_formulaire, views_response, views_test

urlpatterns = [
     #views_formulaire
    path('formulaireList/', views_formulaire.FormulaireList.as_view()),
    path('formulaireDetails/<str:pk>/', views_formulaire.FormulaireDetails.as_view()),

    path('questionList/', views_formulaire.QuestionList.as_view()),
    path('questionDetails/<int:pk>/', views_formulaire.QuestionDetails.as_view()),

    path('checkboxList/', views_formulaire.CheckboxList.as_view()),
    path('checkboxDetails/<int:pk>/', views_formulaire.CheckboxDetails.as_view()),

    path('responseList/', views_response.ResponseList.as_view()),
    path('responseDetails/<int:pk>/', views_response.ResponseDetails.as_view()),


    path('formulaireAllList/', views_formulaire.FormulaireAllList.as_view()),
    path('formulaireAllDetails/<str:pk>/', views_formulaire.FormulaireAllDetails.as_view()),

    path('testList/', views_test.testList.as_view()),

    ]

urlpatterns = format_suffix_patterns(urlpatterns)