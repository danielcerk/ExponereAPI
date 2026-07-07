
from api.catalog.models import Catalog, Link
from api.auth.models import UserProfile

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from django.core.exceptions import ValidationError

User = get_user_model()

class BaseTestCase(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='daniel',
            email='daniel@gmail.com',
            password='1234',
            terms_of_use_is_ready=True
        )

        self.catalog = get_object_or_404(Catalog, user=self.user)

class CatalogTestCase(BaseTestCase):

    def test_get_catalog(self):

        self.assertIsNotNone(self.catalog.pk)

    def test_edit_catalog(self):

        self.catalog.name = 'Lojas Daniel'
        self.catalog.minimum_order_value = 10
        self.catalog.minimum_order_value_free_shipping = 100

        self.catalog.save()

        self.assertEqual(self.catalog.name, 'Lojas Daniel')
        self.assertEqual(self.catalog.minimum_order_value, 10)
        self.assertEqual(self.catalog.minimum_order_value_free_shipping, 100)

    def test_get_invalid_minimu_order_value(self):

        self.catalog.minimum_order_value = -10
        self.catalog.minimum_order_value_free_shipping = -100

        with self.assertRaises(ValidationError):

            self.catalog.full_clean()


class LinkTestCase(BaseTestCase):

    def setUp(self):

        super().setUp()

        self.link = Link.objects.create(
            catalog=self.catalog,
            url="https://instagram.com/teste"
        )

    def test_detect_social_network(self):

        self.assertEqual(self.link.social_name, "instagram")

    def test_invalid_url(self):

        link = Link(catalog=self.catalog, url=None)

        with self.assertRaises(ValidationError):

            link.full_clean()