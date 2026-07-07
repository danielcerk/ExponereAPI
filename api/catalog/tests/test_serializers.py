from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model

from api.auth.serializers import RegisterSerializer
from api.catalog.models import Link, Catalog
from api.catalog.serializers import CatalogSerializer, LinkSerializer

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

        self.assertEqual(self.user.username, 'Daniel')
        self.assertTrue(self.user.check_password('$Trongpassword123'))
        self.assertEqual(self.user.email, 'daniel@example.com')

class CatalogAPITestCase(BaseRegisterAPITestCase):

    def test_get_catalog(self):

        catalog = self.user.catalog

        self.assertIsNotNone(catalog)
        self.assertEqual(catalog.user, self.user)

    def test_edit_catalog(self):

        catalog_data = {

            "name": "Lojas Daniel",
            "minimum_order_value": 10

        }

        serializer = CatalogSerializer(
            self.user, 
            data=catalog_data, 
            partial=True,
            context={'request': self.client}
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        catalog = serializer.save()

        self.assertEqual(catalog.name, 'Lojas Daniel')
        self.assertEqual(catalog.minimum_order_value, 10)

    def test_get_invalid_minimu_order_value(self):

        catalog_data = {

            "minimum_order_value": -10

        }

        serializer = CatalogSerializer(
            self.user, 
            data=catalog_data, 
            partial=True,
            context={'request': self.client}
        )

        self.assertFalse(serializer.is_valid(), serializer.errors)

class LinkAPITestCase(BaseRegisterAPITestCase):

    def test_create_link(self):

        catalog = self.user.catalog

        data = {
            "url": "https://instagram.com/teste"
        }

        serializer = LinkSerializer(
            catalog,
            data=data,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        link = serializer.save(catalog=catalog)

        self.assertEqual(link.catalog, catalog)
        self.assertEqual(link.url, data["url"])

    def test_edit_link(self):

        catalog = self.user.catalog

        link = Link.objects.create(
            catalog=catalog,
            url="https://facebook.com/teste"
        )

        data = {
            "url": "https://youtube.com/teste"
        }

        serializer = LinkSerializer(
            link,
            data=data,
            partial=True,
            context={"catalog": catalog}
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        updated_link = serializer.save()

        self.assertEqual(updated_link.url, data["url"])
        self.assertEqual(updated_link.social_name, "youtube")

    def test_invalid_url(self):

        catalog = self.user.catalog

        data = {
            "url": None
        }

        serializer = LinkSerializer(
            data=data,
            context={"catalog": catalog}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("url", serializer.errors)