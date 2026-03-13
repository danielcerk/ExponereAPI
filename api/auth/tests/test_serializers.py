from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from api.auth.serializers import RegisterSerializer, ProfileSerializer, AccountSerializer

User = get_user_model()

class RegisterSerializerTest(APITestCase):

    def test_create_user_success(self):

        data = {
            'name': 'Daniel',
            'email': 'daniel@example.com',
            'password': 'strongpassword123',
            'terms_of_use_is_ready': True
        }

        serializer = RegisterSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        user = serializer.save()

        self.assertEqual(user.name, 'Daniel')
        self.assertTrue(user.check_password('strongpassword123'))
        self.assertEqual(user.email, 'daniel@example.com')

    def test_create_user_without_email_fails(self):

        data = {
            'name': 'Daniel',
            'password': 'strongpassword123',
            'terms_of_use_is_ready': True
        }

        serializer = RegisterSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

class ProfileSerializerTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            name='Daniel',
            email='daniel@example.com',
            password='password',
            terms_of_use_is_ready=True
        )

    def test_update_profile_address(self):

        profile = self.user.profile
        address_data = {
            'cep': '40301110'
        }
        serializer = ProfileSerializer(profile, data={'address': address_data}, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_profile = serializer.save()
        self.assertEqual(updated_profile.address.cep, '40301110')

class AccountSerializerTest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            name='Daniel',
            email='daniel@gmaile.com',
            password='1234',
            terms_of_use_is_ready=True
        )

    def test_update_name_and_password(self):

        serializer = AccountSerializer(
            self.user, 
            data={'name': 'Dan', 'password': '123'}, 
            partial=True,
            context={'request': self.client}
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        user = serializer.save()

        self.assertEqual(user.name, 'Dan')

        self.assertTrue(user.check_password('123'))

    def test_update_profile_field(self):

        profile_data = {'whatsapp': '+5511999999999'}
        serializer = AccountSerializer(
            self.user,
            data={'profile': profile_data},
            partial=True,
            context={'request': self.client}
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        user = serializer.save()

        self.assertEqual(user.profile.whatsapp, '+5511999999999')
