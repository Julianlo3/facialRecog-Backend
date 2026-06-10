from django.urls import path
from .views import ListarPersonasView
from .views import CrearPersonaView
from .views import ReconocerPersonaView

urlpatterns = [
    path('person/', ListarPersonasView.as_view(), name='listar-personas'),
    path('person/crear/', CrearPersonaView.as_view(), name='crear-persona'),
    path('person/reconocer/', ReconocerPersonaView.as_view(), name='reconocer-persona'),
]