"""from allauth.account.views import confirm_email"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import views_login, views_users, views_admin, views_promo_filiere, views_stage, views_soutenance, views_jury, views_csv, views_import, views_etudiant, views_export, cas, test_cas

urlpatterns = [
    #views_Users
    path('userDetails/<int:pk>/', views_users.UserDetails.as_view()),
    path('userList/', views_users.UserList.as_view()),

    #test_cas
    path('profile/', test_cas.user_profile, name='user_profile'),

    #views_login
    path('changePassword/', views_login.ChangePassword.as_view()),
    path('login/', views_login.CostumLogin.as_view()),
    path('codeReset/', views_login.SendCodeEmail.as_view()),
    path('code/', views_login.gestionCode.as_view()),

    #views_admin
    path('userSearch/', views_admin.GetUser.as_view()),
    path('setAllInactive/', views_admin.SetAllInactive.as_view()),

    #views_promo_filiere
    path('promoDetails/<int:pk>/', views_promo_filiere.PromoDetails.as_view()),
    path('promoList/', views_promo_filiere.PromoList.as_view()),

    path('filiereList/', views_promo_filiere.FiliereList.as_view()),
    path('filiereDetails/<int:pk>/', views_promo_filiere.FiliereDetails.as_view()),

    path('promoFiliere/', views_promo_filiere.PromoFiliere.as_view()),

    #views_stage
    path('stageList/', views_stage.StageList.as_view()),
    path('stageDetails/<int:pk>/', views_stage.StageDetails.as_view()),
    
    #views_soutenance
    path('soutenanceList/', views_soutenance.SoutenanceList.as_view()),
    path('soutenanceDetails/<int:pk>/', views_soutenance.SoutenanceDetails.as_view()),

    #views_jury
    path('juryList/', views_jury.JuryList.as_view()),
    path('juryDetails/<int:pk>/', views_jury.JuryDetails.as_view()),

    #views_etudiant
    path('etudiantAll/<int:pk>/', views_etudiant.EtudiantAll.as_view()),

    #views_import 
    path('importUser/',views_import.importUser.as_view()),
    path('importStage/', views_import.importStage.as_view()),
    path('importSoutenance/', views_import.importSoutenance.as_view()),
    path('importJury/', views_import.importJury.as_view()),

    #views_export
    path("exportNote/", views_export.exportNote.as_view()),
    
    path('', cas.user_cas.as_view())
    ]

urlpatterns = format_suffix_patterns(urlpatterns)