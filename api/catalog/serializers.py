from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from rest_framework import serializers
from .models import  (
    
    Catalog, 
    Link, 

)

from api.cloudinary_utils import ( 
    upload_to_cloudinary_img, 
    delete_from_cloudinary_img
)
class LinkSerializer(serializers.ModelSerializer):

    class Meta:

        model = Link
        fields = [
            "id",
            "catalog",
            "url",
            "social_name",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "catalog",
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            "social_name": {"required": False},
            "catalog": {"required": False}
        }

    def create(self, validated_data):

        catalog = self.context.get("catalog")

        if not catalog:

            view = self.context.get("view")

            if view:

                catalog_id = view.kwargs.get("catalog_pk")
                catalog = get_object_or_404(Catalog, id=catalog_id)

        if not catalog:

            raise ValidationError("Catalog é obrigatório.")

        return Link.objects.create(
            catalog=catalog,
            **validated_data
        )

    def update(self, instance, validated_data):

        for attr, value in validated_data.items():

            setattr(instance, attr, value)

        instance.save()

        return instance

class CatalogSerializer(serializers.ModelSerializer):

    links = LinkSerializer(many=True, required=False)

    photo_file = serializers.ImageField(write_only=True, required=False)
    banner_file = serializers.ImageField(write_only=True, required=False)

    business_category_name = serializers.CharField(
        source="business_category.name",
        read_only=True
    )

    owner_address = serializers.CharField(
        source='user.profile.address',
        read_only=True
    )

    owner_whatsapp = serializers.CharField(
        source='user.profile.whatsapp',
        read_only=True
    )

    owner_cpf_cnpj = serializers.CharField(
        source='user.profile.cpf_cnpj',
        read_only=True
    )
    class Meta:
        model = Catalog
        fields = [
            "id",
            "user",
            "name",
            "slug",
            "photo_img",
            "banner_img",
            "photo_file",
            "banner_file",
            "minimum_order_value",
            "minimum_order_value_free_shipping",
            "business_category",
            "business_category_name",
            "about",
            "owner_address",
            "owner_cpf_cnpj",
            "owner_whatsapp",
            "links",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
            "photo_img",
            "banner_img"
        ]

        extra_kwargs = {
            "photo_img": {"required": False},
            "banner_img": {"required": False},
        }

    def create(self, validated_data):

        photo_file = validated_data.pop("photo_file", None)
        banner_file = validated_data.pop("banner_file", None)

        catalog = Catalog.objects.create(**validated_data)

        if photo_file:

            catalog.photo_img = upload_to_cloudinary_img(photo_file)

        if banner_file:

            catalog.banner_img = upload_to_cloudinary_img(banner_file)

        catalog.save()

        return catalog

    def update(self, instance, validated_data):

        new_photo = validated_data.pop("photo_file", None)
        new_banner = validated_data.pop("banner_file", None)

        if new_photo is not None:

            if instance.photo_img:

                delete_from_cloudinary_img(instance.photo_img)

            instance.photo_img = upload_to_cloudinary_img(new_photo)

        if new_banner is not None:

            if instance.banner_img:

                delete_from_cloudinary_img(instance.banner_img)

            instance.banner_img = upload_to_cloudinary_img(new_banner)

        for attr, value in validated_data.items():

            setattr(instance, attr, value)

        instance.save()

        return instance