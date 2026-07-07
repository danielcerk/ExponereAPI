import requests

from django.core.exceptions import ValidationError

import json

def validate_no_repeated_digits(value):

    if value and len(set(value)) == 1:
        
        raise ValidationError('O CEP não pode conter todos os dígitos iguais.')

def verify_cep(cep: str):

    url = f'https://viacep.com.br/ws/{cep}/json/'

    content = requests.get(url)

    is_ok = True if content.status_code == 200 else False

    return content.json() if is_ok else None

def get_cities(id=None, name=None):

    file_path = "cities.json"

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    cities = data["data"]

    if id is None and name is None:
        return [(city["Nome"], city["Nome"]) for city in cities]

    if id is not None:
        return next((city for city in cities if city["Id"] == id), None)

    if name is not None:
        return next(
            (city for city in cities if city["Nome"].lower() == name.lower()),
            None
        )


def get_states(id=None, UF=None):

    file_path = "states.json"

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    states = data["data"]

    if id is None and UF is None:
        return [(state["Uf"], state["Uf"]) for state in states]

    if id is not None:
        return next((state for state in states if state["Id"] == id), None)

    if UF is not None:
        return next(
            (state for state in states if state["Uf"].lower() == UF.lower()),
            None
        )

if __name__ == '__main__':

    print(verify_cep('40301110'))