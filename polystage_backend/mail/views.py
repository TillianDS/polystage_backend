from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from django.core.mail import send_mail
from django.conf import settings
from back.models import CustomUser, Etudiant, Tuteur, Session
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def getPromoFilireMail(promo, filiere):
    mail = Etudiant.objects.select_related("promo__filiere").filter(promo__filiere__nom = filiere, promo__annee = promo).values_list("email", flat=True)
    return mail

class ChangeMail(APIView):
    def post(self, request, format = None):
        promo = request.data['sujet']
        


class BegginSession(APIView) :

    def mailEtudiant (self, request, email_send, prenom, password):
        subject = 'Ouverture de Polystage'
        context = {
            'prenom' : prenom ,
            'email' : email_send,
            'password' : password
        }
        html_message = render_to_string('email/openPolystageEtudiant.html', context= context)
        plain_message = strip_tags(html_message)

        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, plain_message, from_email, [email_send])

    def mailTuteur(self,request, email):
        subject = 'Ouverture de Polystage'
        
        html_message = render_to_string('email/openPolystageTuteur.html')

        plain_message = strip_tags(html_message)

        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, plain_message, from_email, [email])

    # envoie un mail pour l'ouverture de la plateforme PolyStage
    def post (self, request, pk, format = None) :
        data = request.data

        try : 
            session = Session.objects.get(pk=pk)
        except Session.DoesNotExist:
            return Response({"error" : "la session n'existe pas"})
        
        if session.filiere != request.user.filiere :
            return Response({"error" : "vous ne pouvez pas démarrer cette session"})
        
        for jury in session.jury_set :
            for soutenance in jury.soutenance_set :
                email_etudiant = soutenance.stage.etudiant.email

        #return Response({'success': 'email envoyé avec succès', "mail": email_send}, status=status.HTTP_200_OK)

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