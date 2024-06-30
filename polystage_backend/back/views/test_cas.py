from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import UserSerializer, EnseignantSerializer, TuteurSerializer, ProfessionnelSerializer, AdminSerializer, EtudiantSerializer, PromoSerializer
from rest_framework.permissions import IsAuthenticated
from django_cas_ng.signals import cas_user_authenticated
from django.dispatch import receiver
from .utils import get_cas_client

@login_required
def user_profile(request):
    attributes = request.session.get('attributes', {})
    return render(request, 'user_profile.html', {
        'user': request.user,
        'attributes': attributes,
    })


class getTicket(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        ticket = request.session.get('ticket')
        attributes = request.session.get('attributes', {})
        is_authenticated = request.user.is_authenticated

        # Messages de débogage
        print(f"Ticket récupéré dans la vue: {ticket}")
        print(f"Attributs récupérés: {attributes}")

        return Response({
            "ticket": ticket,
            "attributes": attributes,
            "is_authenticated": is_authenticated
        })
