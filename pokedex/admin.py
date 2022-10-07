from django.contrib import admin

from .models import (
    Ability,
    Pokemon,
    PokemonAbilitySlot,
    PokemonType,
    PokemonTypeSlot
)

# Register your models here.
@admin.register(PokemonType)
class PokemonTypeAdmin(admin.ModelAdmin):
    pass

class PokemonTypeSlotInline(admin.TabularInline):
    model = PokemonTypeSlot


class PokemonAbilitySlotInline(admin.TabularInline):
    model = PokemonAbilitySlot


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    inlines = [
        PokemonTypeSlotInline,
        PokemonAbilitySlotInline
    ]

@admin.register(Ability)
class AbilityAdmin(admin.ModelAdmin):
    pass
