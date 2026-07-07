from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from api.customer.models import Customer
from api.catalog.models import Catalog
from api.address.models import Address

User = get_user_model()

class CustomerModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='daniel',
            email='daniel@gmail.com',
            password='1234',
            terms_of_use_is_ready=True
        )

        self.address = Address.objects.create(

            cep='44067368'

        )

        self.catalog = get_object_or_404(Catalog, user=self.user)

    def test_create_customer_success(self):

        customer = Customer.objects.create(
            catalog=self.catalog,
            address=self.address,
            full_name="Daniel Gomes",
            email="daniel@gmail.com"
        )

        self.assertEqual(customer.full_name, "Daniel Gomes")
        self.assertEqual(customer.email, "daniel@gmail.com")
        self.assertTrue(customer.is_active)
        self.assertFalse(customer.is_integration)

    def test_slug_is_generated_on_save(self):
        customer = Customer.objects.create(
            catalog=self.catalog,
            address=self.address,
            full_name="Daniel Gomes"
        )

        self.assertEqual(customer.slug, "daniel-gomes")

    def test_str_method(self):
        
        customer = Customer.objects.create(
            catalog=self.catalog,
            address=self.address,
            full_name="Daniel Gomes"
        )

        expected = "catalogo - Daniel Gomes"
        self.assertEqual(str(customer), expected)

    def test_valid_cpf(self):

        customer = Customer(
            catalog=self.catalog,
            address=self.address,
            full_name="Cliente CPF",
            cpf_cnpj="123.456.789-10"
        )

        customer.full_clean()

    def test_invalid_cpf_raises_error(self):
        customer = Customer(
            catalog=self.catalog,
            address=self.address,
            full_name="Cliente CPF",
            cpf_cnpj="12345678910"
        )

        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_valid_whatsapp(self):
        customer = Customer(
            catalog=self.catalog,
            address=self.address,
            full_name="Cliente WhatsApp",
            whatsapp="+5575999999999"
        )

        customer.full_clean()

    def test_invalid_whatsapp_raises_error(self):
        customer = Customer(
            catalog=self.catalog,
            address=self.address,
            full_name="Cliente WhatsApp",
            whatsapp="75999999999"
        )

        with self.assertRaises(ValidationError):
            customer.full_clean()