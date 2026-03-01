from rest_framework import serializers
from .models import Catalog, Link

from api.cloudinary_utils import ( 
    upload_to_cloudinary, 
    delete_from_cloudinary
)

class LinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Link
        fields = [
            "id",
            "catalog",
            "url",
            "slug",
            "social_name",
            "is_active",
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
            "slug": {"required": False},
            "social_name": {"required": False},
        }


class CatalogSerializer(serializers.ModelSerializer):

    link = LinkSerializer(required=False)

    class Meta:
        model = Catalog
        fields = [
            "id",
            "user",
            "name",
            "photo_img",
            "banner_img",
            "description",
            "is_active",
            "created_at",
            "updated_at",
            "link",
        ]

        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            "photo_img": {"required": False},
            "banner_img": {"required": False},
        }

    def create(self, validated_data):

        link_data = validated_data.pop("link", None)

        photo_file = validated_data.pop("photo_img", None)
        banner_file = validated_data.pop("banner_img", None)

        catalog = Catalog.objects.create(**validated_data)

        if photo_file:

            catalog.photo_img = upload_to_cloudinary(photo_file)

        if banner_file:

            catalog.banner_img = upload_to_cloudinary(banner_file)

        catalog.save()

        if link_data:

            Link.objects.create(catalog=catalog, **link_data)

        return catalog

    def update(self, instance, validated_data):

        link_data = validated_data.pop("link", None)

        new_photo = validated_data.pop("photo_img", None)
        new_banner = validated_data.pop("banner_img", None)

        if new_photo is not None:

            if instance.photo_img:

                delete_from_cloudinary(instance.photo_img)

            instance.photo_img = upload_to_cloudinary(new_photo)

        if new_banner is not None:

            if instance.banner_img:

                delete_from_cloudinary(instance.banner_img)

            instance.banner_img = upload_to_cloudinary(new_banner)

        for attr, value in validated_data.items():

            setattr(instance, attr, value)

        instance.save()

        if link_data:

            link_instance = getattr(instance, "link", None)

            if link_instance:

                for attr, value in link_data.items():

                    setattr(link_instance, attr, value)

                link_instance.save()

            else:

                Link.objects.create(catalog=instance, **link_data)

        return instance