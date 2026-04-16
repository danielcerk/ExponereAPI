import re
from django.core.exceptions import ValidationError

def validate_no_repeated_chars(value):

    cleaned = re.sub(r'\D', '', value)

    if not cleaned:

        raise ValidationError('Documento inválido.')

    if cleaned == cleaned[0] * len(cleaned):
        raise ValidationError('Inválido: caracteres repetidos.')

    most_common = max(set(cleaned), key=cleaned.count)

    if cleaned.count(most_common) >= len(cleaned) - 1:

        raise ValidationError('Inválido: padrão suspeito.')

    if cleaned in '0123456789' or cleaned in '9876543210':

        raise ValidationError('Inválido: sequência numérica.')

    for size in range(1, len(cleaned)//2 + 1):

        pattern = cleaned[:size]

        if pattern * (len(cleaned)//size) == cleaned:

            raise ValidationError('Inválido: padrão repetitivo.')

    if len(cleaned) == 11:

        for i in range(9, 11):

            soma = sum(int(cleaned[num]) * ((i+1) - num) for num in range(i))
            digito = ((soma * 10) % 11) % 10

            if int(cleaned[i]) != digito:

                raise ValidationError('CPF inválido.')

        return cleaned

    elif len(cleaned) == 14:

        pesos_1 = [5,4,3,2,9,8,7,6,5,4,3,2]
        pesos_2 = [6] + pesos_1

        soma = sum(int(cleaned[i]) * pesos_1[i] for i in range(12))
        dig1 = 11 - (soma % 11)
        dig1 = dig1 if dig1 < 10 else 0

        soma = sum(int(cleaned[i]) * pesos_2[i] for i in range(13))
        dig2 = 11 - (soma % 11)
        dig2 = dig2 if dig2 < 10 else 0

        if int(cleaned[12]) != dig1 or int(cleaned[13]) != dig2:

            raise ValidationError('CNPJ inválido.')

        return cleaned

    else:
        
        raise ValidationError('Documento deve ser CPF ou CNPJ válido.')