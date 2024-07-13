"""from allauth.account.views import confirm_email"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import views_login, views_users, views_admin, views_promo_filiere, views_stage, views_soutenance, views_jury, views_import, views_etudiant, views_export, cas, test_cas, views_test, views_session, views_superUser

urlpatterns = [
    #views_test
    path('test/', views_test.test.as_view()),
    path('get-token/', views_test.get_csrf_token, name='get_csrf_token'),

    #views_Users
    path('userDetails/<int:pk>/', views_users.UserDetails.as_view()),
    path('userList/', views_users.UserList.as_view(), name = 'userList'),
    path('stageTuteur/', views_users.stageTuteur.as_view(), name = 'stageTuteur'),

    #test_cas
    path('profile/', test_cas.user_profile, name='user_profile'),

    #views_login
    path('changePassword/', views_login.ChangePassword.as_view()),
    path('login/', views_login.CostumLogin.as_view(), name = 'login'),
    path('codeReset/', views_login.SendCodeEmail.as_view()),
    path('code/', views_login.gestionCode.as_view()),
    path('logout/', views_login.Logout.as_view(), name='custom_logout'),
    path('setPassword/', views_login.SetPassword.as_view(), name='setPassword'),

    #views_admin
    path('userSearchAllChamp/', views_admin.userSearchAllChamp.as_view()),
    path('userSearch/', views_admin.userSearch.as_view()),
    path('stageSearch/', views_admin.stageSearch.as_view()),
    path('soutenanceSearch/', views_admin.soutenanceSearch.as_view()),

    path('setAllInactive/', views_admin.SetAllInactive.as_view()),

    #views_promo_filiere
    path('sessionDetails/<int:pk>/', views_promo_filiere.SessionDetails.as_view()),
    path('sessionList/', views_promo_filiere.SessionList.as_view()),

    path('filiereList/', views_promo_filiere.FiliereList.as_view()),
    path('filiereDetails/<int:pk>/', views_promo_filiere.FiliereDetails.as_view()),

    path('sessionFiliere/', views_promo_filiere.SessionFiliere.as_view()),
    path('getSessionFiliere/<int:pk>/', views_promo_filiere.getSessionFiliere.as_view()),
    
    #views_session
    path('getInfoSession/<int:pk>/', views_session.getInfoSession.as_view()),
    path('getUserSession/', views_session.getUserSession.as_view()),

    #views_stage
    path('stageList/', views_stage.StageList.as_view()),
    path('stageDetails/<int:pk>/', views_stage.StageDetails.as_view()),
    path('getStageTuteur/', views_stage.getStageTuteur.as_view()),

    #views_soutenance
    path('soutenanceList/', views_soutenance.SoutenanceList.as_view()),
    path('soutenanceDetails/<int:pk>/', views_soutenance.SoutenanceDetails.as_view()),
    path('setNote/', views_soutenance.setNote.as_view()),
  
    #views_jury
    path('juryList/', views_jury.JuryList.as_view()),
    path('juryDetails/<int:pk>/', views_jury.JuryDetails.as_view()),
    path('isJury/', views_jury.isJury.as_view()),
    path('becomeLeader/', views_jury.becomeLeader.as_view()),
    path('isLeader/', views_jury.isLeader.as_view()),
    path('juryAll/<int:pk>/', views_jury.juryAll.as_view()),
    path('getJury/', views_jury.getJury.as_view()),

    #views_etudiant
    path('etudiantAll/', views_etudiant.EtudiantAll.as_view()),

    #views_import 
    path('importUser/',views_import.importUser.as_view()),
    path('importStage/', views_import.importStage.as_view()),
    path('importSoutenance/', views_import.importSoutenance.as_view()),
    path('importJury/', views_import.importJury.as_view()),

    #views_export
    path("exportNote/", views_export.exportNote.as_view()),
    
    path('', cas.user_cas.as_view()),

    #views_superUser
    path('createSuperUser/', views_superUser.createSuperUser.as_view()),

    
    ]

urlpatterns = format_suffix_patterns(urlpatterns)