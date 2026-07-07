from rest_framework.test import APITestCase

from api.address.serializers import AddressSerializer
from api.address.models import Address

class AddressSerializerTestCase(APITestCase):

    def setUp(self):

        self.valid_data = {
            'cep': '44067368'
        }

    def test_update_address(self):

        serializer = AddressSerializer(data=self.valid_data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        address = serializer.save()

        update_data = {
            'cep': '44036900'
        }

        update_serializer = AddressSerializer(instance=address, data=update_data, partial=True)

        self.assertTrue(update_serializer.is_valid(), update_serializer.errors)
        updated_address = update_serializer.save()

        self.assertEqual(updated_address.cep, update_data['cep'])
        self.assertEqual(updated_address.street, 'Avenida Transnordestina')

    def test_create_address_with_invalid_text_cep(self):

        data = {
            'cep': 'XX'
        }

        serializer = AddressSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('cep', serializer.errors)


    def test_create_address_with_invalid_number_cep(self):

        data = {
            'cep': '6589874-%$'
        }

        serializer = AddressSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('cep', serializer.errors)

    def test_delete_address(self):

        serializer = AddressSerializer(data=self.valid_data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        address = serializer.save()

        pk = address.pk
        address.delete()

        self.assertFalse(Address.objects.filter(pk=pk).exists())
