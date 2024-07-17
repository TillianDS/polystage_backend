from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from back.models import *
from back.serializers import * 
from rest_framework import serializers

class List(APIView):

    model : models.Model
    serializer : serializers.ModelSerializer

    def set_attribute(self, set_model, set_serializer):
        self.model = set_model
        self.serializer = set_serializer
        
    def get (self, request, format = None):
        formulaire = self.model.objects.all()
        serializer = self.serializer(formulaire, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post (self, request, format = None):
        serializer = self.serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Details(APIView):
    model : models.Model
    serializer : serializers.ModelSerializer
    nom : str

    def set_attribute(self, set_model, set_serializer, set_nom):
        self.model = set_model
        self.serializer = set_serializer
        self.nom = set_nom
        
    def getInstance(self, pk):
        return self.model.objects.get(pk = pk)
    
    def get (self, request, pk, format = None):
        instance = self.getInstance(pk)
        serializer = self.serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put (self, request, pk, format = None):
        instance = self.getInstance(pk)
        serializer = self.serializer(instance, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format = None):
        instance = self.getInstance(pk)
        instance.delete()
        return Response({'success': 'instance de {nom} supprimée avec succès'.format(nom=self.nom)})
