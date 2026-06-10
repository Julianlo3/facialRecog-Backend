import numpy as np
from django.shortcuts import render

from rest_framework import viewsets
from .models import Persona
from .serializers import PersonaSerializer
from rest_framework import generics
import face_recognition
from rest_framework.views import APIView
from rest_framework.response import Response

class ListarPersonasView(generics.ListAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

class CrearPersonaView(generics.CreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

    def perform_create(self, serializer):
        persona = serializer.save()

        imagen = face_recognition.load_image_file(persona.imagen.path)
        encodings = face_recognition.face_encodings(imagen)

        if len(encodings) > 0:
            persona.embedding = encodings[0].tolist()
            persona.save()


class ReconocerPersonaView(APIView):

    def post(self, request):

        try:

            if 'imagen' not in request.FILES:

                return Response(
                    {
                        "recognized": False,
                        "message": "No se recibió ninguna imagen"
                    },
                    status=400
                )

            imagen = face_recognition.load_image_file(
                request.FILES['imagen']
            )

            print(imagen.shape)

            face_locations = face_recognition.face_locations(imagen)

            print(
                "Rostros detectados:",
                len(face_locations)
            )
            

            encodings = (
                face_recognition.face_encodings(
                    imagen
                )
            )

            if not encodings:

                return Response(
                    {
                        "recognized": False,
                        "message": "No se detectó ningún rostro"
                    }
                )

            encoding_actual = encodings[0]

            mejor_persona = None
            mejor_distancia = 999

            for persona in Persona.objects.all():

                if not persona.embedding:
                    continue

                distancia = (
                    face_recognition.face_distance(
                        [
                            np.array(
                                persona.embedding
                            )
                        ],
                        encoding_actual
                    )[0]
                )

                if distancia < mejor_distancia:

                    mejor_distancia = distancia
                    mejor_persona = persona

            # 0.6 es el umbral recomendado
            if (
                mejor_persona is not None
                and mejor_distancia < 0.6
            ):

                return Response(
                    {
                        "recognized": True,
                        "persona": mejor_persona.nombre,
                        "acceso": mejor_persona.nivelAcceso,
                        "distance": float(
                            mejor_distancia
                        )
                    }
                )

            return Response(
                {
                    "recognized": False,
                    "message": "Persona no reconocida"
                }
            )

        except Exception as e:

            return Response(
                {
                    "recognized": False,
                    "message": str(e)
                },
                status=500
            )