from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Persona
from .serializers import PersonaSerializer
from rest_framework import generics


class ListarPersonasView(generics.ListAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

class CrearPersonaView(generics.CreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer