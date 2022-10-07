from rest_framework import serializers
from pokedex.models import Ability, Pokemon, PokemonAbilitySlot, PokemonTypeSlot

class PokemonTypeSlotSerializer(serializers.ModelSerializer):
    pokemon_type = serializers.CharField()

    class Meta:
        model = PokemonTypeSlot
        fields = [
            'slot',
            'pokemon_type'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['pokemon_type'] = instance.pokemon_type.name

        return representation

class AbilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Ability
        fields = [
            'name',
            'long_effect',
            'short_effect'
        ]

class PokemonAbilitySlotSerializer(serializers.ModelSerializer):
    ability = AbilitySerializer(many=False)

    class Meta:
        model = PokemonAbilitySlot
        fields = '__all__'

class PokemonSerializer(serializers.ModelSerializer):
    pokemon_types = PokemonTypeSlotSerializer(many=True)
    pokemon_abilities = PokemonAbilitySlotSerializer(many=True)

    class Meta:
        model = Pokemon
        fields = [
            'name',
            'base_experience',
            'height',
            'order',
            'weight',
            'pokemon_types',
            'pokemon_abilities',
            'sprite_url',
            'official_image_url'
        ]
