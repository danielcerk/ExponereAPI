from rest_framework import serializers

from django.utils.text import slugify

from .models import Keyword

class KeywordSerializer(serializers.ModelSerializer):

    class Meta:

        model = Keyword
        fields = '__all__'
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at')

    def validate_keyword(self, value):
        value = value.lower().strip()

        if len(value) < 2:
            raise serializers.ValidationError("Palavra-chave muito curta.")

        return value

    def validate(self, data):
        keyword = data.get("keyword", getattr(self.instance, "keyword", None))
        catalog = data.get("catalog", getattr(self.instance, "catalog", None))

        if Keyword.objects.filter(
            catalog=catalog,
            keyword__iexact=keyword
        ).exclude(
            pk=self.instance.pk if self.instance else None
        ).exists():
            raise serializers.ValidationError({
                "keyword": "Essa palavra-chave já existe neste catálogo."
            })

        return data

    def create(self, validated_data):
        keyword = validated_data.get("keyword")
        validated_data["keyword"] = keyword.lower().strip()

        if not validated_data.get("slug"):
            validated_data["slug"] = slugify(validated_data["keyword"])

        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "keyword" in validated_data:
            validated_data["keyword"] = validated_data["keyword"].lower().strip()
            validated_data["slug"] = slugify(validated_data["keyword"])

        return super().update(instance, validated_data)