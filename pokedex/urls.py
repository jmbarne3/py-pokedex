from django.urls import path, include
from pokedex.views import PokemonViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'pokemon', PokemonViewset)


urlpatterns = [
    path('', include(router.urls)),
]
