from django.db import models

# Create your models here.
class Ability(models.Model):
    pokeapi_id = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False, db_index=True)
    long_effect = models.TextField(null=True, blank=True)
    short_effect = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()

class PokemonType(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, db_index=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()

class Pokemon(models.Model):
    pokeapi_id = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False, db_index=True)
    base_experience = models.IntegerField(null=False, blank=False)
    height = models.IntegerField(null=False, blank=False)
    order = models.IntegerField(null=False, blank=False)
    weight = models.IntegerField(null=False, blank=False)
    official_image_url = models.URLField(null=True, blank=True)
    sprite_url =models.URLField(null=True, blank=True)
    base_hp = models.IntegerField(null=False, blank=False, default=0)
    effort_hp = models.IntegerField(null=False, blank=False, default=0)
    base_attack = models.IntegerField(null=False, blank=False, default=0)
    effort_attack = models.IntegerField(null=False, blank=False, default=0)
    base_defense = models.IntegerField(null=False, blank=False, default=0)
    effort_defense = models.IntegerField(null=False, blank=False, default=0)
    base_special_attack = models.IntegerField(null=False, blank=False, default=0)
    effort_special_attack = models.IntegerField(null=False, blank=False, default=0)
    base_special_defense = models.IntegerField(null=False, blank=False, default=0)
    effort_special_defense = models.IntegerField(null=False, blank=False, default=0)
    base_speed = models.IntegerField(null=False, blank=False, default=0)
    effort_speed = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()


class PokemonTypeSlot(models.Model):
    slot = models.IntegerField(null=False, blank=False)
    pokemon = models.ForeignKey(Pokemon, null=False, blank=False, on_delete=models.CASCADE, related_name="pokemon_types")
    pokemon_type = models.ForeignKey(PokemonType, null=False, blank=False, on_delete=models.CASCADE, related_name="pokemon")

    def __str__(self):
        return f"{self.pokemon.name} - {self.pokemon_type.name}"

    def __unicode__(self):
        return self.__str__()

class PokemonAbilitySlot(models.Model):
    slot = models.IntegerField(null=False, blank=False)
    pokemon = models.ForeignKey(Pokemon, null=False, blank=False, on_delete=models.CASCADE, related_name='pokemon_abilities')
    ability = models.ForeignKey(Ability, null=False, blank=False, on_delete=models.CASCADE, related_name='pokemon')

    def __str__(self):
        return f"{self.pokemon.name} - {self.ability.name}"

    def __unicode__(self):
        return self.__str__()
