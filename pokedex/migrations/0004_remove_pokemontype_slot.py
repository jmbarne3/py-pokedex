# Generated by Django 4.1.2 on 2022-10-06 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0003_ability_remove_pokemon_types_pokemontypeslot_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemontype',
            name='slot',
        ),
    ]
