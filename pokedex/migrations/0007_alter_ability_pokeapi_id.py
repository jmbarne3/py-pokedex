# Generated by Django 4.1.2 on 2022-10-06 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0006_ability_pokeapi_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ability',
            name='pokeapi_id',
            field=models.IntegerField(),
        ),
    ]
