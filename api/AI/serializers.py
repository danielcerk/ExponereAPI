from rest_framework import serializers

from .models import CopyProduct

from google import genai

client = genai.Client()

def generate_copy(content):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
    Crie uma copy persuasiva de marketing para o seguinte produto:

    {content}

    Instruções:
    - Destaque benefícios claros e práticos (não apenas características).
    - Utilize gatilhos mentais como escassez, urgência, prova social e autoridade, quando fizer sentido.
    - Linguagem simples, direta e envolvente.
    - Estruture o texto de forma fluida (pode usar pequenos parágrafos ou listas curtas).
    - Foque em conversão (como se fosse para página de vendas ou anúncio).

    Restrições:
    - NÃO inclua introduções como "Aqui está", "Segue abaixo", etc.
    - NÃO explique o que você está fazendo.
    - NÃO use títulos como "Copy:" ou similares.
    - Retorne APENAS o texto final da copy.

    Objetivo:
    Gerar um texto convincente que aumente o interesse e a chance de compra do produto.
    """
    )

    return content

class GenerateCopySerializer(serializers.Serializer):

    copy = serializers.SerializerMethodField()

    def get_copy(self, obj):

        copy_input = self.context.get("copy")

        return generate_copy(copy_input)

class CopyProductSerializer(serializers.ModelSerializer):

    class Meta:

        model = CopyProduct
        fields = '__all__'