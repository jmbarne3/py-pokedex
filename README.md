# Pokedex API

This project endeavors to create a searchable, robust representation of the [Pokeapi.co](https://pokeapi.co/) data for use in personal projects. I find I often want an interesting, large dataset in which to experiment with when learning new frontend frameworks, and I have absolutely loved using the Pokeapi for those projects. However, there are a few limitations, as in the inability to perform a simple searches based on Pokemon names or other attributes directly from the Pokemon endpoint. This project adds some of those features, as well as simplifies the data structure to one more in tune with my own tastes.

## Project Setup

1. Create a virtual environment with python3: `python3 -m venv pokeapi`
2. Clone in this repository: `cd pokeapi && git clone https://github.com/jmbarne3/py-pokeapi src`
3. Activate the virtual environment and install requirements: `cd src && source ../bin/activate && pip install -r requirements.txt`
4. Copy `pokeapi/settings_local.templ.py` to `pokeapi/settings_local.py` and update values as needed.
5. Run initial migrations and import data: `python manage.py setup`
6. Launch the API locally: `python manage.py runserver`

