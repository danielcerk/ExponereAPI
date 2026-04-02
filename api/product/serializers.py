from rest_framework import serializers

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

from api.cloudinary_utils import upload_to_cloudinary_img, delete_from_cloudinary_img

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
            'product': {'required': True}
        }

    def validate(self, data):

        product = data.get('product') or getattr(self.instance, 'product', None)

        if not product:

            raise serializers.ValidationError("Produto é obrigatório.")

        count = Image.objects.filter(product=product).count()

        if not self.instance and count >= 3:

            raise serializers.ValidationError(

                "Este produto já possui o máximo de 3 imagens."

            )

        return data

    def _handle_upload(self, validated_data):

        image_file = validated_data.pop('image_upload', None)

        if image_file:

            validated_data['image'] = upload_to_cloudinary_img(
                image_file,
                'product_images'
            )

        return validated_data

    def create(self, validated_data):

        validated_data = self._handle_upload(validated_data)

        return super().create(validated_data)

    def update(self, instance, validated_data):

        validated_data = self._handle_upload(validated_data)

        return super().update(instance, validated_data)
    
class ProductSerializer(serializers.ModelSerializer):

    images = ImageSerializer(many=True, required=False)
    product_logistic_info = ProductLogisticInfoSerializer(required=False)
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        required=False
    )

    subcategories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=SubCategory.objects.all(),
        required=False
    )
    stock = StockSerializer(required=False)

    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'slug': {'read_only': True},
            'is_active': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def create(self, validated_data):
        
        request = self.context.get('request')

        validated_data['user'] = request.user

        categories_data = validated_data.pop("categories", [])
        subcategories_data = validated_data.pop("subcategories", [])
        images_data = validated_data.pop("images", [])
        logistic_data = validated_data.pop("product_logistic_info", None)
        stock_data = validated_data.pop("stock", None)

        product = Product.objects.create(**validated_data)

        if categories_data:

            product.categories.set(categories_data)

        if subcategories_data:

            product.subcategories.set(subcategories_data)

        if logistic_data:

            ProductLogisticInfo.objects.create(product=product, **logistic_data)

        if stock_data:

            StockSerializer().create({**stock_data, "product": product})

        for image_data in images_data:

            image_data['product'] = product
            ImageSerializer().create(image_data)

        return product

    def update(self, instance, validated_data):

        request = self.context.get('request')

        categories_data = validated_data.pop("categories", None)
        subcategories_data = validated_data.pop("subcategories", None)
        logistic_data = validated_data.pop("product_logistic_info", None)
        stock_data = validated_data.pop("stock", None)

        for attr, value in validated_data.items():

            setattr(instance, attr, value)

        instance.save()

        if categories_data is not None:

            instance.categories.set(categories_data)

        if subcategories_data is not None:

            instance.subcategories.set(subcategories_data)

        if logistic_data:

            ProductLogisticInfo.objects.update_or_create(
                product=instance,
                defaults=logistic_data
            )

        if stock_data:

            if hasattr(instance, 'stock') and instance.stock:

                StockSerializer().update(instance.stock, stock_data)

            else:
                
                StockSerializer().create({**stock_data, "product": instance})

        keep_image_ids = request.data.getlist('keep_images')

        if keep_image_ids:

            instance.images.exclude(id__in=keep_image_ids).delete()

        else:

            instance.images.all().delete()

        images_files = request.FILES.getlist('images')

        for image in images_files:

            ImageSerializer().create({
                "product": instance,
                "image_upload": image
            })

        return instance