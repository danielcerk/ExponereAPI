from django.test import TestCase

from django.contrib.auth import get_user_model

User = get_user_model()


class UserTestCase(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(

            name='daniel', email='daniel@gmail.com',
            password='1234', terms_of_use_is_ready=True

        )

        return super().setUp()
    
    def test_get_user_profile(self):

        self.assertEqual(self.user.name, 'daniel')
        self.assertEqual(self.user.profile.slug, 'daniel')

    def test_create_user_without_email(self):

        with self.assertRaises(ValueError) as context:

            User.objects.create_user(
                name='daniel',
                password='1234', terms_of_use_is_ready=True
            )

        self.assertIn('email', str(context.exception))


    def test_update_name_user(self):

        self.user.name = 'daniela'
        self.user.save()

        self.assertEqual('daniela', self.user.name)

    def test_delete_user(self):

        self.user.delete()

        self.assertEqual(User.objects.count(), 0)