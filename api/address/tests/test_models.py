from django.test import TestCase

from ..models import Address

class AddressTestCase(TestCase):

    def setUp(self):

        self.address = Address.objects.create(

            cep='44067368'

        )

    def test_get_address(self):

        address_count = Address.objects.count()

        self.assertEqual(address_count, 1)
        self.assertEqual(self.address.cep, '44067368')

    def test_update_address(self):

        self.address.cep = '40301110'
        self.address.save()

        self.assertEqual(self.address.cep, '40301110')

    def test_delete_address(self):

        self.address.delete()

        self.assertEqual(Address.objects.count(), 0)