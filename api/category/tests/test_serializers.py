from rest_framework.test import APITestCase
from types import SimpleNamespace

from django.contrib.auth import get_user_model

from api.auth.serializers import RegisterSerializer
from api.catalog.models import Catalog
from api.category.models import Category, SubCategory, BusinessCategory
from api.category.serializers import (
    CategorySerializer,
    SubCategorySerializer,
    BusinessCategorySerializer
)

User = get_user_model()


class BaseRegisterAPITestCase(APITestCase):

    def setUp(self):

        data = {
            'username': 'Daniel',
            'email': 'daniel@example.com',
            'password': '$Trongpassword123',
            'terms_of_use_is_ready': True
        }

        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        self.user = serializer.save()
        self.catalog = self.user.catalog


class BusinessCategorySerializerTestCase(APITestCase):

    def test_create_business_category(self):

        data = {"name": "Restaurantes"}

        serializer = BusinessCategorySerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        instance = serializer.save()

        self.assertEqual(instance.name, "Restaurantes")
        self.assertIsNotNone(instance.slug)

class CategorySerializerTestCase(BaseRegisterAPITestCase):

    def get_mock_view(self):
        return SimpleNamespace(kwargs={"catalog_pk": self.catalog.id})

    def test_create_category(self):

        data = {"name": "Eletrônicos"}

        serializer = CategorySerializer(
            data=data,
            context={"view": self.get_mock_view()}
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        category = serializer.save()

        self.assertEqual(category.name, "Eletrônicos")
        self.assertEqual(category.catalog, self.catalog)

    def test_edit_category(self):

        category = Category.objects.create(
            catalog=self.catalog,
            name="Roupas"
        )

        data = {"name": "Roupas Atualizadas"}

        serializer = CategorySerializer(
            category,
            data=data,
            partial=True,
            context={"view": self.get_mock_view()}
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        updated = serializer.save()

        self.assertEqual(updated.name, "Roupas Atualizadas")

    def test_invalid_empty_name(self):

        data = {"name": "   "}

        serializer = CategorySerializer(
            data=data,
            context={"view": self.get_mock_view()}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_duplicate_category_name(self):

        Category.objects.create(
            catalog=self.catalog,
            name="Beleza"
        )

        data = {"name": "Beleza"}

        serializer = CategorySerializer(
            data=data,
            context={"view": self.get_mock_view()}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)


class SubCategorySerializerTestCase(BaseRegisterAPITestCase):

    def setUp(self):
        super().setUp()

        self.category = Category.objects.create(
            catalog=self.catalog,
            name="Tecnologia"
        )

    def get_mock_view(self):

        return SimpleNamespace(kwargs={"category_pk": self.category.id})

    def test_create_subcategory(self):

        data = {"name": "Celulares"}

        serializer = SubCategorySerializer(
            data=data,
            context={"view": self.get_mock_view()}
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        sub = serializer.save()

        self.assertEqual(sub.name, "Celulares")
        self.assertEqual(sub.category, self.category)

    def test_edit_subcategory(self):

        sub = SubCategory.objects.create(
            category=self.category,
            name="Notebooks"
        )

        data = {"name": "Notebooks Gamer"}

        serializer = SubCategorySerializer(
            sub,
            data=data,
            partial=True,
            context={"view": self.get_mock_view()}
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        updated = serializer.save()

        self.assertEqual(updated.name, "Notebooks Gamer")

    def test_duplicate_subcategory_name(self):

        SubCategory.objects.create(
            category=self.category,
            name="Acessórios"
        )

        data = {"name": "Acessórios"}

        serializer = SubCategorySerializer(
            data=data,
            context={
                "view": self.get_mock_view(),
                "category": self.category
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_invalid_empty_name(self):

        data = {"name": "   "}

        serializer = SubCategorySerializer(
            data=data,
            context={"view": self.get_mock_view()}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)