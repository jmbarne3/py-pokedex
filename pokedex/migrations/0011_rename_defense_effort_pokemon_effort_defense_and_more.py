# Generated by Django 4.1.2 on 2022-10-10 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0010_pokemon_base_attack_pokemon_base_defense_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pokemon',
            old_name='defense_effort',
            new_name='effort_defense',
        ),
        migrations.RenameField(
            model_name='pokemon',
            old_name='special_attack_effort',
            new_name='effort_special_attack',
        ),
        migrations.RenameField(
            model_name='pokemon',
            old_name='special_defense_effort',
            new_name='effort_special_defense',
        ),
        migrations.RenameField(
            model_name='pokemon',
            old_name='speed_effort',
            new_name='effort_speed',
        ),
    ]