from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from django.core.mail import send_mail
from django.conf import settings
from back.models import CustomUser, Etudiant, Tuteur, Session
from formulaire.models import Formulaire, StatusFormulaire
from back.serializers import TuteurSerializer
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from back.views.password import *
from polystage_backend.permissions import *


class ChangeMail(APIView):
    def post(self, request, format = None):
        promo = request.data['sujet']
class OpenSession(APIView) :
    permission_classes = [IsAuthenticated, AdminPermission]

    def mailEtudiant (self, email_send, prenom, nom):
        subject = 'Ouverture de Polystage'
        context = {
            'prenom' : prenom ,
            'nom' : nom,
            'email' : email_send,
        }
        html_message = render_to_string('email/openPolystageEtudiant.html', context= context)
        plain_message = strip_tags(html_message)

        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, plain_message, from_email, [email_send])

    def mailEtudiantFirstCo (self, email_send, prenom, password, nom):
        subject = 'Ouverture de Polystage'
        context = {
            'prenom' : prenom ,
            'nom' : nom,
            'email' : email_send,
            'password' : password
        }
        html_message = render_to_string('email/openPolystageEtudiantFirstCo.html', context= context)
        plain_message = strip_tags(html_message)

        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, plain_message, from_email, [email_send])

    def mailTuteur(self, email, nom, prenom, lien):
        subject = 'Ouverture de Polystage'
        context = {
            'prenom' : prenom ,
            'nom' : nom,
            'lien' : lien ,
        }
        html_message = render_to_string('email/openPolystageTuteur.html', context)

        plain_message = strip_tags(html_message)

        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, plain_message, from_email, [email])

    # envoie un mail pour l'ouverture de la plateforme PolyStage
    def post (self, request, pk, format = None) :
        try : 
            session = Session.objects.get(pk=pk)
        except Session.DoesNotExist:
            return Response({"error" : "la session n'existe pas"})
        
        if session.filiere != request.user.instance.filiere :
            return Response({"error" : "vous ne pouvez pas démarrer cette session"})
        
        etudiants = Etudiant.objects.filter(stage__soutenance__jury__session = session).distinct()
        tuteurs = Tuteur.objects.filter(stage__soutenance__jury__session = session).distinct()
        errors = []
        for etudiant in etudiants :
            formulaires_etudiants = Formulaire.objects.filter(session=session, profile = 'ETU')
            if etudiant.first_connection:
                password = generate_password()
                try :
                    self.mailEtudiantFirstCo(email_send= etudiant.email, nom=etudiant.last_name, prenom=etudiant.first_name, password=password )
                except :
                    errors.append({"etudiant" :etudiant})
                etudiant.set_password(password)
                etudiant.save()
            else :
                try :
                    self.mailEtudiant(email_send=etudiant.email, nom=etudiant.last_name, prenom=etudiant.first_name)
                except :
                    errors.append({"etudiant": etudiant})
            for formulaire in formulaires_etudiants :
                pass

        for tuteur in tuteurs :
            lien = ""
            self.mailTuteur(email=tuteur.email, nom=tuteur.last_name, prenom=tuteur.first_name, lien=lien)

        return Response({'success': "les mails ont été envoyés avec succès"}, status=status.HTTP_200_OK)

def mailConfirmationForm (email_send, titre_form) :

    subject = 'Confirmation de validation du Formulaire'
    context = {
        'titre_form' : titre_form
    }
    html_message = render_to_string('email/confirmationForm.html', context)
    plain_message = strip_tags(html_message)

    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, plain_message, from_email, [email_send])
    return Response({'success': 'email envoyé avec succès'})
    
def mailSauvegardeForm (email_send, titre_form) :

    subject = 'confirmation de modification'
    context = {
        'titre_form' : titre_form
    }
    html_message = render_to_string('email/sauvegardeForm.html', context)
    plain_message = strip_tags(html_message)

    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, plain_message, from_email, [email_send])
    return Response({'success': 'email envoyé avec succès'})

def sendVerificationCode(email_send, code):
    subject = 'Réinitialiser votre mot de passe'
    context = {
        'code' : code
    }
    html_message = render_to_string('email/confirmationForm.html', context)
    plain_message = strip_tags(html_message)
    
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, plain_message, from_email, [email_send])
