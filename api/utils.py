import re
from django.core.exceptions import ValidationError

def validate_no_repeated_chars(value):

    cleaned = re.sub(r'\W', '', value)

    if len(set(cleaned)) == 1:

        raise ValidationError('Documento inválido: não pode conter caracteres repetidos.')