"""from allauth.account.views import confirm_email"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import views_formulaire, views_question
urlpatterns = [
     #views_formulaire
    path('formulaireList/', views_formulaire.FormulaireList.as_view()),
    path('formulaireDetails/<str:pk>/', views_formulaire.FormulaireDetails.as_view()),

    #views_question
    path('questionList/', views_question.QuestionList.as_view()),
    path('questionDetails/<int:pk>/', views_question.QuestionList.as_view()),


    ]

urlpatterns = format_suffix_patterns(urlpatterns)