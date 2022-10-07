from email.mime import base
from typing import Any, Dict, Optional
from django.core.management.base import BaseCommand, CommandError, CommandParser

from threading import Thread, Lock
from queue import Queue

import requests
from progress.bar import ChargingBar

from pokedex.models import(
    Ability,
    Pokemon,
    PokemonAbilitySlot,
    PokemonType,
    PokemonTypeSlot
)

class Command(BaseCommand):
    help = 'Imports pokemon from Pokeapi.co'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--pokeapi-url',
            type=str,
            help='The Base URL of the Pokeapi',
            dest='base_url',
            default='https://pokeapi.co/api/v1'
        )

        parser.add_argument(
            '--max-threads',
            type=int,
            help='The maximum number of threads to spawn',
            dest='max_threads',
            default=5
        )


    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.base_url = options['base_url']
        self.max_threads = options['max_threads']
        self.mt_lock = Lock()
        self.db_lock = Lock()

        self.created = 0
        self.updated = 0
        self.types_created = 0

        self.get_pokemon_list()
        self.get_pokemon_data()
        self.stdout.write(self.style.SUCCESS("Successfully imported pokemon!"))


    def get_pokemon_list(self):
        """
        Runs through the pages of pokemon and gets the URL
        of their details API location.
        """
        self.resource_list = []

        next_url = f"{self.base_url}/pokemon"

        while next_url != None:
            response = requests.get(next_url)
            if response.ok:
                data = response.json()
                next_url = data['next']
                self.resource_list += data['results']


    def get_pokemon_data(self):
        """
        Runs through the list of individual pokemon
        API URLs and pulls down the data.
        """
        self.resource_queue = Queue()

        for resource in self.resource_list:
            self.resource_queue.put(resource)

        self.pokemon_bar = ChargingBar(
            'Fetching Pokemon data...',
            max=self.resource_queue.qsize()
        )

        for _ in range(self.max_threads):
            Thread(target=self.__get_pokemon_data_worker, daemon=True).start()

        self.resource_queue.join()


    def __get_pokemon_data_worker(self):
        """
        Worker function for retrieving Pokemon data
        """
        while True:
            try:
                resource = self.resource_queue.get()

                url = resource['url']
                response = requests.get(url)

                if response.ok:
                    self.__save_pokemon(response.json())

                with self.mt_lock:
                    self.pokemon_bar.next()
            except Exception as e:
                self.stderr.write(self.style.ERROR(e))
            finally:
                self.resource_queue.task_done()

    def __save_pokemon(self, data: Dict):
        """
        Saves a pokemon given the data returned
        from the Pokeapi
        """
        pokeapi_id: int = data['id']
        name: str = self.__format_name(data['name'], True)
        base_experience: str = data['base_experience'] if data['base_experience'] is not None else 0
        height: int = data['height']
        order: int = data['order']
        weight: int = data['weight']
        types = data['types']
        abilities = data['abilities']

        sprite_url = data['sprites']['front_default']
        official_image_url = None

        if 'official-artwork' in data['sprites']['other'] and \
            len(data['sprites']['other']['official-artwork']) > 0:
            official_image_url = data['sprites']['other']['official-artwork']['front_default']

        pokemon = None

        with self.db_lock:
            try:
                pokemon = Pokemon.objects.get(pokeapi_id=pokeapi_id)
                pokemon.name = name
                pokemon.base_experience = base_experience
                pokemon.height = height
                pokemon.order = order
                pokemon.weight = weight
                pokemon.sprite_url = sprite_url
                pokemon.official_image_url = official_image_url
                pokemon.save()

                self.updated += 1
            except Pokemon.DoesNotExist:
                pokemon = Pokemon(
                    pokeapi_id=pokeapi_id,
                    name=name,
                    base_experience=base_experience,
                    height=height,
                    order=order,
                    weight=weight,
                    sprite_url=sprite_url,
                    official_image_url=official_image_url
                )
                pokemon.save()

                self.created += 1

        for pt in types:
            dpt = self.__get_or_create_pokemon_type(pt, pokemon)
            pokemon.pokemon_types.add(dpt)

        for pa in abilities:
            dpa = self.__get_or_create_pokemon_ability(pa, pokemon)
            pokemon.pokemon_abilities.add(dpa)


    def __format_name(self, name: str, parenthesis: bool = False) -> str:
        div_name = name.split('-')
        div_name = list(map(str.capitalize, div_name))

        if len(div_name) > 1 and parenthesis:
            return f"{div_name[0]} ({' '.join(div_name[1:])})"

        return ' '.join(div_name)


    def __get_or_create_pokemon_type(self, type_data: Any, pokemon: Pokemon) -> PokemonTypeSlot:
        """
        Gets or creates the pokemon type
        """
        name: str = type_data['type']['name']
        slot: int = type_data['slot']

        with self.db_lock:
            pt: PokemonType = None

            try:
                pt = PokemonType.objects.get(name=name.capitalize())
            except PokemonType.DoesNotExist:
                pt = PokemonType(name=name.capitalize())
                pt.save()
                self.types_created += 1

            try:
                pts = PokemonTypeSlot.objects.get(slot=slot, pokemon=pokemon, pokemon_type=pt)
                return pts
            except PokemonTypeSlot.DoesNotExist:
                pts = PokemonTypeSlot(
                    slot=slot,
                    pokemon=pokemon,
                    pokemon_type=pt
                )
                pts.save()
                return pts


    def __get_or_create_pokemon_ability(self, ability_data: Any, pokemon: Pokemon) -> PokemonAbilitySlot:
        """
        Gets or creates the pokemon ability
        """
        url = ability_data['ability']['url']

        response = requests.get(url)

        if not response.ok:
            return None

        data = response.json()

        pokeapi_id: int = data['id']
        name: str = self.__format_name(data['name'])
        long_effect: str = ""
        short_effect: str = ""

        slot: int = ability_data['slot']

        if len(data['effect_entries']) > 0:
            for ee in data['effect_entries']:
                if ee['language']['name'] == 'en':
                    long_effect = ee['effect']
                    short_effect = ee['short_effect']

        ab = None

        with self.db_lock:
            try:
                ab = Ability.objects.get(pokeapi_id=pokeapi_id)
                ab.name = name
                ab.long_effect = long_effect
                ab.short_effect = short_effect
                ab.save()
            except Ability.DoesNotExist:
                ab = Ability(
                    pokeapi_id=pokeapi_id,
                    name=name,
                    long_effect=long_effect,
                    short_effect=short_effect
                )
                ab.save()

            try:
                pas = PokemonAbilitySlot.objects.get(slot=slot, pokemon=pokemon, ability=ab)
                return pas
            except PokemonAbilitySlot.DoesNotExist:
                pas = PokemonAbilitySlot(
                    slot=slot,
                    pokemon=pokemon,
                    ability=ab
                )
                pas.save()
                return pas
