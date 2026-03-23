from rest_framework import serializers

from .models import CopyProduct

from google import genai

client = genai.Client()

def generate_copy(content):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f'Responda de maneira triste a esse conteúdo: {content}',
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