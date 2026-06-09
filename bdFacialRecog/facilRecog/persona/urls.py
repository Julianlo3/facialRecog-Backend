from django.urls import path
from .views import ListarPersonasView
from .views import CrearPersonaView

urlpatterns = [
    path('person/', ListarPersonasView.as_view(), name='listar-personas'),
    path('person/crear/', CrearPersonaView.as_view(), name='crear-persona'),
]