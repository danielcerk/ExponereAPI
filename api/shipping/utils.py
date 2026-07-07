import requests

from django.conf import settings

from .models import ShippingStatus

MELHOR_ENVIO_CLIENT_ID = settings.MELHOR_ENVIO_CLIENT_ID
MELHOR_ENVIO_CLIENT_SECRET = settings.MELHOR_ENVIO_CLIENT_SECRET

access_token = settings.MELHOR_ENVIO_ACCESS_TOKEN

# https://sandbox.melhorenvio.com.br/api/v2/me/shipment/calculate
# https://sandbox.melhorenvio.com.br/api/v2/me/shipment/tracking < -- Achar alguma API de rastreamento

base_url = "https://sandbox.melhorenvio.com.br/api/v2/me/shipment/"

def _make_request(url, method="GET", data=None):

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Exponere (contato@marketilize.com.br)"
    }

    if method == "POST":

        response = requests.post(url, json=data, headers=headers)

    else:

        response = requests.get(url, headers=headers)

    if response.status_code not in [200, 201]:

        raise Exception(response.json())

    return response.json()

def shipment_calculate(postal_code_from: str, postal_code_to: str, products: list):

    url = f"{base_url}calculate"

    payload = {
        "from": {
            "postal_code": postal_code_from
        },
        "to": {
            "postal_code": postal_code_to
        },
        "products": products,
        "options": {
            "receipt": False,
            "own_hand": False
        }
    }

    return _make_request(url, method="POST", data=payload)

def shipment_tracking():

    # Ver como vou puxar esses dados ( Webhook )
    # Salvar todas as atualizações no models ShippingStatus

    pass