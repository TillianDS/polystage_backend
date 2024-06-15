from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from django.core.mail import send_mail
from django.conf import settings
from back.models import CustomUser, Etudiant, Tuteur
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def getPromoFilireMail(promo, filiere):
    mail = Etudiant.objects.select_related("promo__filiere").filter(promo__filiere__nom = filiere, promo__annee = promo).values_list("email", flat=True)
    return mail

class sendMailOpenPolystage(APIView) :
    # envoie un mail pour l'ouverture de la plateforme AMU Stage
    def post (self, request, format = None) :
        data = request.data

        if 'promo' not in data :
            return Response({'error': "vous devez renseigner l'année d'un promotion"}, status=status.HTTP_400_BAD_REQUEST)
        if 'filiere' not in data :
            return Response({'error': "vous devez renseigner le nom d'une filiere"}, status=status.HTTP_400_BAD_REQUEST)
        
        promo = data['promo']
        filiere = data['filiere']

        #on cherche les mail des tous les étudiants correspondant au nom de la fileire et à l'année de la promo voulu
        email_send = getPromoFilireMail(promo, filiere)
        
        
        subject = 'Ouverture de Polystage'
        html_message = render_to_string('email/openPolystage.html')
        plain_message = strip_tags(html_message)

        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, plain_message, from_email, email_send)

        return Response({'success': 'email envoyé avec succès', "mail": email_send}, status=status.HTTP_200_OK)

class confirmationForm (APIView) :
    def post (self, request, format = None):
        
        if 'email' not in request.data :
            return Response({'error': "vous devez renseigner un mail"}, status=status.HTTP_400_BAD_REQUEST)
       
        email_send = request.data['email']

        subject = 'Confirmation de validation du Formulaire'
        html_message = render_to_string('email/confirmationForm.html')
        plain_message = strip_tags(html_message)

        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, plain_message, from_email, [email_send])
        return Response({'success': 'email envoyé avec succès'})
    
class modificationForm (APIView) :
    def post (self, request, format = None):
        
        if 'email' not in request.data :
            return Response({'error': "vous devez renseigner un mail"}, status=status.HTTP_400_BAD_REQUEST)
       
        email_send = request.data['email']

        subject = 'confirmation de modification'
        html_message = render_to_string('email/modificationForm.html')
        plain_message = strip_tags(html_message)

        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, plain_message, from_email, [email_send])
        return Response({'success': 'email envoyé avec succès'})