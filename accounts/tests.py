import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Account

superuser_data = {'username': 'adminuser', 'password': 'adminuserpass'}
staffuser1_data = {'username': 'staff1', 'password': 'staff1pass'}
staffuser2_data = {'username': 'staff2', 'password': 'staff2pass'}

accounts_list_url = reverse('accounts')
account_create_url = reverse('account-create')
account_detail_url = reverse('account-detail', kwargs={'id': 1})
account_update_url = reverse('account-update', kwargs={'id': 1})
account_delete_url = reverse('account-delete', kwargs={'id': 1})
account_password_change_url = reverse('account-change-password', kwargs={'id': 1})


class APITestCaseWithSetUp(APITestCase):
    """
    setUp for Account Related Tests
    Create 3 Account, 1 Superuser and 2 Staffuser
    Authorize With Created Superuser Access Token
    """

    def setUp(self):
        self.superuser = Account.objects.create_superuser(**superuser_data)
        self.staffuser = Account.objects.create_user(**staffuser1_data)
        self.staffuser2 = Account.objects.create_user(**staffuser2_data)
        # get created superuser tokens with rest_framework_simplejwt TokenObtainPair View
        admin_auth = self.client.post(reverse('token_obtain_pair'), superuser_data).data
        # Authorization with access token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + admin_auth['access'])


class AccountCreateTestCase(APITestCase):

    def test_account_create(self):
        response = self.client.post(account_create_url, superuser_data)
        user_date = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user_date['username'], superuser_data['username'])

    def test_account_create_invalid_data(self):
        response = self.client.post(account_create_url, {'username': 'testuser', 'password': 'p'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AccountListTestCase(APITestCaseWithSetUp):

    def test_superuser(self):
        response = self.client.get(accounts_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staffuser(self):
        self.client.force_authenticate(user=self.staffuser)
        response = self.client.get(accounts_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(accounts_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AccountDetailTestCase(APITestCaseWithSetUp):

    def test_account_detail_by_superuser(self):
        response = self.client.get(account_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_account_detail_by_owner(self):
        url = reverse('account-detail', kwargs={'id': self.staffuser.id})
        self.client.force_authenticate(user=self.staffuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_account_detail_by_other_account(self):
        url = reverse('account-detail', kwargs={'id': self.staffuser.id})
        self.client.force_authenticate(user=self.staffuser2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_account_detail_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(account_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AccountUpdateTestCase(APITestCaseWithSetUp):

    def test_account_update_by_superuser(self):
        response = self.client.put(account_update_url, {'username': 'new_username'})
        user_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_data['username'], 'new_username')

    def test_account_update_by_owner(self):
        url = reverse('account-update', kwargs={'id': self.staffuser.id})
        self.client.force_authenticate(user=self.staffuser)
        response = self.client.put(url, {'gender': 'Male'})
        user_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_data['gender'], 'Male')

    def test_account_update_by_other_user(self):
        url = reverse('account-update', kwargs={'id': self.staffuser.id})
        self.client.force_authenticate(user=self.staffuser2)
        response = self.client.put(url, {'gender': 'Male'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_account_update_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.put(account_update_url, {'gender': 'Male'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_account_update_invalid_data(self):
        response = self.client.put(account_update_url, {'email': 'invalid email'})
        user_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AccountDeleteTestCase(APITestCaseWithSetUp):
    def test_account_delete_by_superuser(self):
        response = self.client.delete(account_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_account_delete_by_staffuser(self):
        self.client.force_authenticate(user=self.staffuser)
        response = self.client.delete(account_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_account_delete_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.put(account_delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AccountPasswordChangeTestCase(APITestCaseWithSetUp):

    def test_account_password_change_by_owner(self):
        url = reverse('account-change-password', kwargs={'id': self.staffuser.id})
        self.client.force_authenticate(user=self.staffuser)
        data = {'old_password': staffuser1_data['password'], 'password1': 'newpassword', 'password2': 'newpassword'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_account_password_change_by_other_user(self):
        url = reverse('account-change-password', kwargs={'id': self.staffuser.id})
        data = {'old_password': staffuser1_data['password'], 'password1': 'newpassword', 'password2': 'newpassword'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_account_password_change_unauthorized(self):
        self.client.force_authenticate(user=None)
        data = {'old_password': staffuser1_data['password'], 'password1': 'newpassword', 'password2': 'newpassword'}
        response = self.client.put(account_password_change_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_account_password_change_invalid_data(self):
        url = reverse('account-change-password', kwargs={'id': self.superuser.id})
        data = {'old_password': 'some_wrong_psw', 'password1': 'newpassword', 'password2': 'newpassword'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
