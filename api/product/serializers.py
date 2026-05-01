from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework import serializers

from api.catalog.models import Catalog
from .models import ( 
    Image,
    Product,
    ProductLogisticInfo,

)
from api.category.models import (

    Category, SubCategory

)
from api.category.serializers import ( 
    
    CategorySerializer,
    SubCategorySerializer

)
from api.stock.serializers import StockSerializer
from api.cloudinary_utils import upload_to_cloudinary_img
from api.stock.models import StockMovement, Stock

class ProductLogisticInfoSerializer(serializers.ModelSerializer):

    class Meta:

        model = ProductLogisticInfo
        fields = '__all__'

        read_only_fields = (

            'id', 'product', 
            'created_at', 'updated_at'

        )

class ImageSerializer(serializers.ModelSerializer):

    image_upload = serializers.ImageField(write_only=True, required=False)

    class Meta:

        model = Image
        fields = '__all__'

        read_only_fields = ('id',)
        extra_kwargs = {
            'product': {'required': False}
        }

    def validate(self, data):

        product = (
            data.get('product')
            or getattr(self.instance, 'product', None)
            or self.context.get('product')
        )

        if not product:

            return data

        return data

    def _handle_upload(self, validated_data):

        image_file = validated_data.pop('image_upload', None)

        if image_file:

            validated_data['image'] = upload_to_cloudinary_img(
                image_file
            )

        return validated_data

    def create(self, validated_data):

        validated_data = self._handle_upload(validated_data)

        return super().create(validated_data)

    def update(self, instance, validated_data):

        validated_data = self._handle_upload(validated_data)

        return super().update(instance, validated_data)

class ProductSerializer(serializers.ModelSerializer):

    logistic_info = ProductLogisticInfoSerializer(
        required=False,
    )

    stocks = StockSerializer(
        required=False,
    )

    category = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        required=False
    )

    subcategory = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=SubCategory.objects.all(),
        required=False
    )

    images = ImageSerializer(many=True)

    class Meta:
        
        model = Product
        fields = '__all__'
        read_only_fields = (
            'id', 'slug', 'catalog', 'is_active', 'created_at', 'updated_at'
        )

    def validate(self, data):

        request = self.context.get('request')
        images_files = request.FILES.getlist('images')

        instance = getattr(self, 'instance', None)
        current_count = instance.images.count() if instance else 0

        if current_count + len(images_files) > 3:

            raise serializers.ValidationError({
                "images": "Máximo de 3 imagens por produto."
            })

        return data

    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get('request')

        logistic_data = validated_data.pop('logistic_info', None)
        stock_data = validated_data.pop('stocks', None)
        categories = validated_data.pop('category', [])
        subcategories = validated_data.pop('subcategory', [])
        images_data = validated_data.pop('images', [])

        catalog = get_object_or_404(Catalog, user=request.user)

        product = Product.objects.create(
            catalog=catalog,
            **validated_data
        )

        if categories:
            product.category.set(categories)

        if subcategories:
            product.subcategory.set(subcategories)

        if logistic_data:
            ProductLogisticInfo.objects.create(
                product=product,
                **logistic_data
            )

        if stock_data:
            movement_data = stock_data.pop('movement', None)

            stock = Stock.objects.create(
                product=product,
                **stock_data
            )

            if movement_data:
                StockMovement.objects.create(
                    stock=stock,
                    **movement_data
                )

        for image_data in images_data:

            Image.objects.create(
                product=product,
                **image_data
            )

        images_files = request.FILES.getlist('images')

        for image in images_files:

            ImageSerializer().create({
                "product": product,
                "image_upload": image
            })

        return product
    

    @transaction.atomic
    def update(self, instance, validated_data):
        request = self.context.get('request')

        logistic_data = validated_data.pop('logistic_info', None)
        stock_data = validated_data.pop('stocks', None)
        categories = validated_data.pop('category', None)
        subcategories = validated_data.pop('subcategory', None)
        images_data = validated_data.pop('images', None)

        for attr, value in validated_data.items():

            setattr(instance, attr, value)

        instance.save()

        if categories is not None:

            instance.category.set(categories)

        if subcategories is not None:

            instance.subcategory.set(subcategories)

        if logistic_data:

            ProductLogisticInfo.objects.update_or_create(
                product=instance,
                defaults=logistic_data
            )

        if stock_data:

            movement_data = stock_data.pop('movement', None)

            stock, created = Stock.objects.get_or_create(
                product=instance,
                defaults=stock_data
            )

            if not created:

                for attr, value in stock_data.items():

                    setattr(stock, attr, value)

                stock.save()

            if movement_data:

                StockMovement.objects.create(
                    stock=stock,
                    **movement_data
                )

        keep_ids = request.data.get('keep_images', None)

        if keep_ids is not None:

            if keep_ids:

                instance.images.exclude(id__in=keep_ids).delete()

            else:

                instance.images.all().delete()

        if images_data:

            for image_data in images_data:

                Image.objects.create(
                    product=instance,
                    **image_data
                )

        images_files = request.FILES.getlist('images')

        for image in images_files:

            ImageSerializer().create({
                "product": instance,
                "image_upload": image
            })

        return instance