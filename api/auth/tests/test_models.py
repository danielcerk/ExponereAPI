from django.test import TestCase

from django.contrib.auth import get_user_model

from api.address.models import Address

from django.core.exceptions import ValidationError

User = get_user_model()

class UserTestCase(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(

            username='daniel', email='daniel@gmail.com',
            password='1234', terms_of_use_is_ready=True

        )

        return super().setUp()
    
    def test_get_user_profile(self):

        self.assertEqual(self.user.username, 'daniel')
        self.assertEqual(self.user.profile.slug, 'daniel')

    def test_create_user_without_email(self):

        with self.assertRaises(ValueError) as context:

            User.objects.create_user(
                username='daniel',
                password='1234', terms_of_use_is_ready=True
            )

        self.assertIn('email', str(context.exception))


    def test_update_name_user(self):

        self.user.username = 'daniela'
        self.user.save()

        self.assertEqual('daniela', self.user.username)

    def test_delete_user(self):

        self.user.delete()

        self.assertEqual(User.objects.count(), 0)