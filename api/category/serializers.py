from rest_framework import serializers
from .models import Category, BusinessCategory, SubCategory

from api.catalog.models import Catalog

from django.shortcuts import get_object_or_404

class BusinessCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessCategory
        fields = [
            "id",
            "name",
            "slug",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "slug",
            "created_at",
            "updated_at",
        ]

class SubCategorySerializer(serializers.ModelSerializer):

    category = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:

        model = SubCategory

        fields = [
            "id",
            "category",
            "name",
            "slug",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "slug",
            "category",
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            "id": {"required": False},
            "slug": {"required": False},
            "category": {"required": False},
        }

    def create(self, validated_data):

        category_id = self.context["view"].kwargs.get("category_pk")

        category = get_object_or_404(Category, id=category_id)

        subcategory = SubCategory.objects.create(
            category=category,
            **validated_data
        )

        return subcategory

    def update(self, instance, validated_data):

        for attr, value in validated_data.items():

            setattr(instance, attr, value)

        instance.save()

        return instance


    def validate(self, attrs):

        category = attrs.get("category") or self.context.get("category")
        name = attrs.get("name")

        if category and name:

            qs = SubCategory.objects.filter(
                category=category,
                name__iexact=name
            )

            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise serializers.ValidationError(
                    {"name": "Já existe uma subcategoria com esse nome nesta categoria."}
                )

        return attrs


class CategorySerializer(serializers.ModelSerializer):

    subcategories = SubCategorySerializer(
        many=True,
        required=False
    )

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
            "subcategories",
        ]

        read_only_fields = [
            "id",
            "catalog",
            "slug",
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            "id": {"required": False},
            "catalog": {"required": False},
            "slug": {"required": False},
        }

    def create(self, validated_data):

        catalog_id = self.context["view"].kwargs.get("catalog_pk")

        catalog = get_object_or_404(Catalog, id=catalog_id)

        category = Category.objects.create(
            catalog=catalog,
            **validated_data
        )

        return category

    def update(self, instance, validated_data):

        for attr, value in validated_data.items():

            setattr(instance, attr, value)

        instance.save()

        return instance

    def validate_name(self, value):

        if not value.strip():
            raise serializers.ValidationError(
                "O nome da categoria não pode estar vazio."
            )

        return value

    def validate(self, attrs):

        catalog = (
            getattr(self.instance, "catalog", None)
            or self.context.get("catalog")
            or getattr(self.context.get("view"), "kwargs", {}).get("catalog_pk")
        )

        name = attrs.get("name")

        if catalog and name:

            qs = Category.objects.filter(
                catalog=catalog,
                name__iexact=name
            )

            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise serializers.ValidationError({
                    "name": "Já existe uma categoria com esse nome neste catálogo."
                })

        return attrs
    

