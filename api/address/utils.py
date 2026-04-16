import requests

from django.core.exceptions import ValidationError

def validate_no_repeated_digits(value):

    if value and len(set(value)) == 1:
        
        raise ValidationError('O CEP não pode conter todos os dígitos iguais.')

def verify_cep(cep: str):

    url = f'https://viacep.com.br/ws/{cep}/json/'

    content = requests.get(url)

    is_ok = True if content.status_code == 200 else False

    return content.json() if is_ok else None

if __name__ == '__main__':

    print(verify_cep('40301110'))