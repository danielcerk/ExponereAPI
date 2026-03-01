from rest_framework import serializers

from .models import ( 
    Advertisement, 
    Category, 
    Feature,
    AdvertisementFeature,
    ImageAdvertisement
)

from api.supabase_utils import upload_to_supabase

class ImageAdvertisementSerializer(serializers.ModelSerializer):

    image_upload = serializers.ImageField(write_only=True, required=False)

    class Meta:

        model = ImageAdvertisement
        fields = '__all__'

        read_only_fields = ('id',)
        extra_kwargs = {
            'advertisement': {'required': False}
        }

    def create(self, validated_data):

        image_file = validated_data.pop('image_upload', None)

        if image_file:

            validated_data['image'] = upload_to_supabase(image_file, 'advertisement_images')

        return super().create(validated_data)

    def update(self, instance, validated_data):

        image_file = validated_data.pop('image_upload', None)

        if image_file:

            validated_data['image'] = upload_to_supabase(image_file, 'advertisement_images')

        return super().update(instance, validated_data)
    
class AdvertisementSerializer(serializers.ModelSerializer):
    
    images = ImageAdvertisementSerializer(many=True, required=False)

    class Meta:
        model = Advertisement
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'slug': {'read_only': True},
            'is_active': {'read_only': True},
            'expiry_date': {'read_only': True},
            'deletion_date': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def create(self, validated_data):
        
        request = self.context.get('request')
        validated_data['user'] = request.user

        features_data = validated_data.pop("advertisement_features", [])
        validated_data.pop("images", None)

        advertisement = Advertisement.objects.create(**validated_data)

        images_files = request.FILES.getlist('images')

        for img in images_files:
            ImageAdvertisement.objects.create(
                advertisement=advertisement,
                image=upload_to_supabase(img, 'advertisement_images')
            )

        for f in features_data:

            AdvertisementFeature.objects.create(
                advertisement=advertisement,
                feature=f["feature"],
                value=f["value"]
            )

        return advertisement

    def update(self, instance, validated_data):

        request = self.context.get('request')

        features_data = validated_data.pop("advertisement_features", None)

        for attr, value in validated_data.items():

            setattr(instance, attr, value)

        instance.save()

        keep_image_ids = request.data.getlist('keep_images')

        if keep_image_ids:

            instance.images.exclude(id__in=keep_image_ids).delete()

        images_files = request.FILES.getlist('images')

        for img in images_files:
            ImageAdvertisement.objects.create(
                advertisement=instance,
                image=upload_to_supabase(img, 'advertisement_images')
            )

        if features_data is not None:

            instance.advertisement_features.all().delete()

            for f in features_data:

                AdvertisementFeature.objects.create(
                    advertisement=instance,
                    feature=f["feature"],
                    value=f["value"]
                )

        return instance