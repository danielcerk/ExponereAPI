from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APIRequestFactory

from api.product.serializers import (
    ProductSerializer,
    ImageSerializer,
    ProductLogisticInfoSerializer,
)
from api.product.models import Product, Image, ProductLogisticInfo
from api.category.models import Category, SubCategory
from api.stock.models import Stock


User = get_user_model()


class ProductSerializerTest(TestCase):

    def setUp(self):

        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="123456"
        )

        self.catalog = self.user.catalog

        self.category = Category.objects.create(
            catalog=self.catalog,
            name="Calças"
        )

        self.subcategory = SubCategory.objects.create(
            category=self.category,
            name="Skinny"
        )

        self.request = self.factory.post("/products/")
        self.request.user = self.user

    def test_create_product_serializer(self):
        data = {
            "title": "Calça Skinny",
            "description": "Produto teste",
            "price": Decimal("99.90"),
            "category": [self.category.id],
            "subcategory": [self.subcategory.id],
            "images": [
                {
                    "image": "https://placehold.co/600"
                }
            ],
            "logistic_info": {
                "weight": Decimal("0.500"),
                "height": Decimal("10.00"),
                "width": Decimal("20.00"),
                "length": Decimal("30.00"),
            },
            "stocks": {
                "quantity": 10,
                "min_quantity": 2
            }
        }

        serializer = ProductSerializer(
            data=data,
            context={"request": self.request}
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        product = serializer.save()

        self.assertEqual(product.title, "Calça Skinny")
        self.assertEqual(product.images.count(), 1)
        self.assertTrue(hasattr(product, "logistic_info"))
        self.assertTrue(hasattr(product, "stocks"))

    def test_update_product_serializer(self):
        product = Product.objects.create(
            catalog=self.catalog,
            title="Produto antigo",
            description="teste"
        )

        Image.objects.create(
            product=product,
            image="https://placehold.co/600"
        )

        request = self.factory.patch("/products/")
        request.user = self.user
        request.data = {
            "keep_images": []
        }

        data = {
            "title": "Produto atualizado",
            "images": [
                {
                    "image": "https://placehold.co/400"
                }
            ]
        }

        serializer = ProductSerializer(
            product,
            data=data,
            partial=True,
            context={"request": request}
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        updated = serializer.save()

        self.assertEqual(updated.title, "Produto atualizado")
        self.assertEqual(updated.images.count(), 1)

    def test_validate_max_images(self):
        product = Product.objects.create(
            catalog=self.catalog,
            title="Produto teste",
            description="teste"
        )

        for _ in range(3):
            Image.objects.create(
                product=product,
                image="https://placehold.co/600"
            )

        request = self.factory.patch("/products/")
        request.user = self.user
        request.FILES.setlist(
            "images",
            [
                SimpleUploadedFile(
                    "test.jpg",
                    b"file_content",
                    content_type="image/jpeg"
                )
            ]
        )

        serializer = ProductSerializer(
            product,
            data={"title": "Novo"},
            partial=True,
            context={"request": request}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("images", serializer.errors)


class ImageSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="imageuser",
            email="image@test.com",
            password="123456"
        )

        self.catalog = self.user.catalog

        self.product = Product.objects.create(
            catalog=self.catalog,
            title="Produto imagem",
            description="teste"
        )

    def test_create_image_serializer_with_url(self):
        serializer = ImageSerializer(
            data={
                "product": self.product.id,
                "image": "https://placehold.co/600"
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        image = serializer.save()

        self.assertEqual(image.product, self.product)

class ProductLogisticInfoSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="logisticuser",
            email="logistic@test.com",
            password="123456"
        )

        self.catalog = self.user.catalog

        self.product = Product.objects.create(
            catalog=self.catalog,
            title="Produto",
            description="teste"
        )

    def test_create_logistic_serializer(self):
        serializer = ProductLogisticInfoSerializer(
            data={
                "weight": Decimal("0.500"),
                "height": Decimal("10.00"),
                "width": Decimal("20.00"),
                "length": Decimal("30.00")
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_update_logistic_serializer(self):
        logistic = ProductLogisticInfo.objects.create(
            product=self.product,
            weight=Decimal("0.500")
        )

        serializer = ProductLogisticInfoSerializer(
            logistic,
            data={"weight": Decimal("1.000")},
            partial=True
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        updated = serializer.save()

        self.assertEqual(updated.weight, Decimal("1.000"))


class NestedStockSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="stockuser",
            email="stock@test.com",
            password="123456"
        )

        self.catalog = self.user.catalog

    def test_create_product_with_stock(self):
        request = APIRequestFactory().post("/products/")
        request.user = self.user

        serializer = ProductSerializer(
            data={
                "title": "Produto estoque",
                "description": "teste",
                "images": [
                    {
                        "image": "https://placehold.co/600"
                    }
                ],
                "stocks": {
                    "quantity": 20,
                    "min_quantity": 5
                }
            },
            context={"request": request}
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        product = serializer.save()

        self.assertTrue(
            Stock.objects.filter(product=product).exists()
        )