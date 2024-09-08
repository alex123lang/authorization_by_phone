import os
import django

# Устанавливаем путь к файлу настроек
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Инициализация Django
django.setup()


from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from referral_app.models import UserProfile
from referral_app.serializers import UserProfileSerializer


class ReferralAppTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_home_page(self):
        response = self.client.get(reverse('referral_app:home'))
        self.assertEqual(response.status_code, 200)

    def test_create_valid_user_profile(self):
        data = {"phone_number": "1234567890"}
        response = self.client.post(reverse('referral_app:register'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(UserProfile.objects.filter(phone_number='1234567890').exists())

    def test_create_invalid_user_profile_missing_phone_number(self):
        data = {}
        response = self.client.post(reverse('referral_app:register'), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('phone_number', response.data)

    def test_create_invalid_user_profile_duplicate_phone_number(self):
        # Create a user with a phone number
        UserProfile.objects.create(phone_number="1234567890")

        # Try to create another user with the same phone number
        data = {"phone_number": "1234567890"}
        response = self.client.post(reverse('referral_app:register'), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('phone_number', response.data)

    def test_update_auth_code_for_existing_user(self):
        # Create a user
        user = UserProfile.objects.create(phone_number="1234567890")

        # Update the auth code for the user
        data = {"phone_number": "1234567890"}
        response = self.client.put(reverse('referral_app:sign_up', args=[user.pk]), data=data)
        self.assertEqual(response.status_code, 200)

    def test_update_auth_code_for_nonexistent_user(self):
        # Try to update the auth code for a nonexistent user
        data = {"phone_number": "1234567890"}
        response = self.client.put(reverse('referral_app:sign_up', args=[1]), data=data)
        self.assertEqual(response.status_code, 404)

    def test_update_auth_code_for_user_with_missing_phone_number(self):
        # Create a user
        user = UserProfile.objects.create(phone_number="1234567890")

        # Try to update the auth code for the user with a missing phone number
        data = {}
        response = self.client.put(reverse('referral_app:sign_up', args=[user.pk]), data=data)
        self.assertEqual(response.status_code, 400)

    def test_validate_user_login(self):
        data = {"phone_number": "1234567890"}
        user = self.client.post(reverse('referral_app:register'), data=data, format='json')
        # Login the user
        data = {"phone_number": "1234567890", "auth_code": user.data['auth_code']}
        response = self.client.post(reverse('referral_app:login'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

    def test_validate_user_login_with_missing_auth_code(self):
        data = {"phone_number": "1234567890"}
        user = self.client.post(reverse('referral_app:register'), data=data, format='json')
        # Login the user
        data = {"phone_number": "1234567890"}
        response = self.client.post(reverse('referral_app:login'), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('auth_code', response.data)

    def test_validate_user_login_with_invalid_auth_code(self):
        data = {"phone_number": "1234567890"}
        user = self.client.post(reverse('referral_app:register'), data=data, format='json')
        # Login the user
        data = {"phone_number": "1234567890", "auth_code": "invalid_auth_code"}
        response = self.client.post(reverse('referral_app:login'), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('auth_code', response.data)

    def test_validate_user_login_with_missing_phone_number(self):
        data = {"phone_number": "1234567890"}
        user = self.client.post(reverse('referral_app:register'), data=data, format='json')
        # Login the user
        data = {"auth_code": user.data['auth_code']}
        response = self.client.post(reverse('referral_app:login'), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('phone_number', response.data)

    def test_validate_user_login_with_invalid_phone_number(self):
        data = {"phone_number": "1234567890"}
        user = self.client.post(reverse('referral_app:register'), data=data, format='json')
        # Login the user
        data = {"phone_number": "invalid_phone_number", "auth_code": user.data['auth_code']}
        response = self.client.post(reverse('referral_app:login'), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('phone_number', response.data)

    def test_retrieve_user_profile(self):
        # Create a user
        data_registration = {"phone_number": "1234567890"}
        user = self.client.post(reverse('referral_app:register'), data=data_registration, format='json')

        # Login the user
        data_login = {"phone_number": "1234567890", "auth_code": user.data['auth_code']}
        response_login = self.client.post(reverse('referral_app:login'), data=data_login)

        # Retrieve the user profile
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response_login.data["access"]}')
        response = self.client.get(reverse('referral_app:retrieve', args=[user.data['id']]))
        self.assertEqual(response.status_code, 200)

    def test_retrieve_user_used_invite_code(self):
        # Create the users
        data_registration_1 = {"phone_number": "1234567890"}
        user_1 = self.client.post(reverse('referral_app:register'), data=data_registration_1, format='json')

        data_registration_2 = {"phone_number": "9876543210"}
        user_2 = self.client.post(reverse('referral_app:register'), data=data_registration_2, format='json')

        # Login the user
        data_login = {"phone_number": "1234567890", "auth_code": user_1.data['auth_code']}
        response_login = self.client.post(reverse('referral_app:login'), data=data_login)

        # Retrieve the user profile
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response_login.data["access"]}')

        data = {"invite_used": user_2.data['invite_code']}
        response = self.client.patch(reverse('referral_app:retrieve', args=[user_1.data['id']]), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('invite_used', response.data)