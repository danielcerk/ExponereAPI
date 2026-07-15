from rest_framework import serializers

from .models import NewsletterEmail

class NewsletterEmailSerializer(serializers.ModelSerializer):

    class Meta:

        model = NewsletterEmail
        fields = '__all__'

    def validate_email(self, value):

        if NewsletterEmail.objects.filter(email__iexact=value).exists():

            raise serializers.ValidationError(

                "Este e-mail já está cadastrado na newsletter."

            )
        
        return value