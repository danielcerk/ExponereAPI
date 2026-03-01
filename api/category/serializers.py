from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category

        fields = [
            "id",
            "catalog",
            "name",
            "slug",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "catalog",
            "slug",
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {

            'id': {'required': False},
            'catalog': {'required': False},
            'slug': {'required': False}

        }


    def validate_name(self, value):

        if not value.strip():
            raise serializers.ValidationError(
                "O nome da categoria não pode estar vazio."
            )
        return value

    def validate(self, attrs):

        catalog = attrs.get("catalog")
        name = attrs.get("name")

        if catalog and name:

            qs = Category.objects.filter(
                catalog=catalog,
                name__iexact=name
            )

            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise serializers.ValidationError(
                    {"name": "Já existe uma categoria com esse nome neste catálogo."}
                )

        return attrs