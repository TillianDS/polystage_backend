"""from allauth.account.views import confirm_email"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import views_formulaire, views_response, views_gestionForm

urlpatterns = [
     #views_formulaire
    path('formulaireList/', views_formulaire.FormulaireList.as_view()),
    path('formulaireDetails/<str:pk>/', views_formulaire.FormulaireDetails.as_view()),

    path('questionList/', views_formulaire.QuestionList.as_view()),
    path('questionDetails/<int:pk>/', views_formulaire.QuestionDetails.as_view()),

    path('checkboxList/', views_formulaire.CheckboxList.as_view()),
    path('checkboxDetails/<int:pk>/', views_formulaire.CheckboxDetails.as_view()),

    path('formulaireSearch/', views_formulaire.FormulaireSearch.as_view()),
    path('retrieveFormulaire/', views_formulaire.retrieveFormulaire.as_view()),
    path('selfFormulaire/', views_formulaire.SelfFormulaire.as_view()),

    path('createFormulaireAll/', views_formulaire.CreateFormulaireAll.as_view()),
    path('getFormulaireAll/<str:pk>/', views_formulaire.GetFormulaireAll.as_view()),

    #views_response
    path('responseList/', views_response.ResponseList.as_view()),
    path('responseDetails/<int:pk>/', views_response.ResponseDetails.as_view()),

    path('responseCheckboxList/', views_response.ResponseCheckboxList.as_view()),
    path('responseCheckboxDetails/<int:pk>/', views_response.ResponseCheckboxDetails.as_view()),
    path('responseFormulaire/', views_response.responseFormulaire.as_view()),


    path('formUser/', views_response.formUser.as_view()),

    #views gestionForm
    path('validateFormulaire/', views_gestionForm.validateFormulaire.as_view()),

    ]

urlpatterns = format_suffix_patterns(urlpatterns)