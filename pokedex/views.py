from django.shortcuts import render
from pokedex.filters import PokemonFilterSet
from pokedex.models import Pokemon
from pokedex.serializers import PokemonSerializer

from rest_framework import viewsets, pagination

# Create your views here.
class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 25
    page_size_query_param = 'limit'
    max_page_size = 100


class PokemonViewset(viewsets.ReadOnlyModelViewSet):
    """
    Provides list and retrieve views for pokemon
    """
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = PokemonFilterSet
