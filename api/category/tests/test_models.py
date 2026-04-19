
from api.catalog.models import Catalog, Link
from api.category.models import Category, SubCategory, BusinessCategory
from api.auth.models import UserProfile

from django.db import IntegrityError
from django.utils.text import slugify
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from django.core.exceptions import ValidationError

User = get_user_model()

class BaseCategoryTestCase(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='daniel',
            email='daniel@gmail.com',
            password='1234',
            terms_of_use_is_ready=True
        )

        self.catalog = get_object_or_404(Catalog, user=self.user)

class BusinessCategoryTestCase(TestCase):

    def test_create_business_category(self):

        category = BusinessCategory.objects.create(name="Restaurantes")

        self.assertEqual(category.name, "Restaurantes")
        self.assertEqual(category.slug, slugify("Restaurantes"))

    def test_slug_uniqueness(self):

        c1 = BusinessCategory.objects.create(name="Loja")
        c2 = BusinessCategory.objects.create(name="Loja")

        self.assertNotEqual(c1.slug, c2.slug)
        self.assertTrue(c2.slug.startswith(c1.slug))

class CategoryTestCase(BaseCategoryTestCase):

    def test_create_category(self):

        category = Category.objects.create(
            catalog=self.catalog,
            name="Eletrônicos"
        )

        self.assertEqual(category.name, "Eletrônicos")
        self.assertEqual(category.slug, slugify("Eletrônicos"))
        self.assertTrue(category.is_active)

    def test_unique_category_per_catalog(self):

        Category.objects.create(
            catalog=self.catalog,
            name="Roupas"
        )

        with self.assertRaises(IntegrityError):
            Category.objects.create(
                catalog=self.catalog,
                name="Roupas"
            )

    def test_unique_slug_per_catalog(self):

        Category.objects.create(
            catalog=self.catalog,
            name="Casa"
        )

        with self.assertRaises(IntegrityError):
            Category.objects.create(
                catalog=self.catalog,
                name="Casa"
            )

    def test_same_name_different_catalog(self):

        user2 = User.objects.create_user(
            username='joao',
            email='joao@gmail.com',
            password='1234',
            terms_of_use_is_ready=True
        )

        catalog2 = Catalog.objects.get(user=user2)

        c1 = Category.objects.create(
            catalog=self.catalog,
            name="Beleza"
        )

        c2 = Category.objects.create(
            catalog=catalog2,
            name="Beleza"
        )

        self.assertEqual(c1.name, c2.name)
        
class SubCategoryTestCase(BaseCategoryTestCase):

    def setUp(self):
        super().setUp()

        self.category = Category.objects.create(
            catalog=self.catalog,
            name="Tecnologia"
        )

    def test_create_subcategory(self):

        sub = SubCategory.objects.create(
            category=self.category,
            name="Celulares"
        )

        self.assertEqual(sub.name, "Celulares")
        self.assertEqual(sub.slug, slugify("Celulares"))
        self.assertTrue(sub.is_active)

    def test_unique_subcategory_per_category(self):

        SubCategory.objects.create(
            category=self.category,
            name="Notebooks"
        )

        with self.assertRaises(IntegrityError):
            SubCategory.objects.create(
                category=self.category,
                name="Notebooks"
            )

    def test_unique_slug_per_category(self):

        SubCategory.objects.create(
            category=self.category,
            name="Acessórios"
        )

        with self.assertRaises(IntegrityError):
            SubCategory.objects.create(
                category=self.category,
                name="Acessórios"
            )

    def test_same_name_different_category(self):

        category2 = Category.objects.create(
            catalog=self.catalog,
            name="Casa"
        )

        s1 = SubCategory.objects.create(
            category=self.category,
            name="Promoções"
        )

        s2 = SubCategory.objects.create(
            category=category2,
            name="Promoções"
        )

        self.assertEqual(s1.name, s2.name)