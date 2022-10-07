from django_filters import rest_framework as filters
from pokedex.models import Pokemon

class PokemonFilterSet(filters.FilterSet):
    search = filters.CharFilter(field_name='name', lookup_expr='icontains')
    primary_type = filters.CharFilter(method='primary_pokemon_type_search', label='Primary Type')
    secondary_type = filters.CharFilter(method='secondary_pokemon_type_search', label='Secondary Type')

    class Meta:
        model = Pokemon
        fields = [
            'name',
            'search'
        ]

    def primary_pokemon_type_search(self, queryset, name, value):
        return queryset.filter(
            pokemon_types__pokemon_type__name__iexact=value,
            pokemon_types__slot=1
        )

    def secondary_pokemon_type_search(self, queryset, name, value):
        return queryset.filter(
            pokemon_types__pokemon_type__name__iexact=value,
            pokemon_types__slot=2
        )
