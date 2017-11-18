# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from user.factories import UserFactory

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient, force_authenticate

from user.views import UserListCreateView, UserRetrieveUpdateDestroyView
from user.models import User

# Create your tests here.

class UserTests(APITestCase):

    # User Manager
    def test_user_by_natural_key_found(self):
        email_user = 'test@test.com'
        email_test = 'test@test.com'
        user = UserFactory.create(email=email_user)
        self.assertIsNotNone(User.objects.get_by_natural_key(email_test))

    def test_user_by_natural_key_not_found(self):
        email_user = 'test1@test.com'
        email_test = 'test2@test.com'
        user = UserFactory.create(email=email_user)

        with self.assertRaises(User.DoesNotExist):
            User.objects.get_by_natural_key(email_test)

    def test_create_user_success(self):
        user = UserFactory.create()
        self.assertNotEqual(len(User.objects.all()), 0)

    def test_create_user_email_non_existant(self):
        with self.assertRaises(ValueError):
            user = UserFactory.create(email=None)
        self.assertEqual(len(User.objects.all()), 0)

    def test_create_superuser_success(self):
        user = UserFactory.create_superuser(email='test@test.com', password='test')
        self.assertNotEqual(len(User.objects.all()), 0)

    def test_create_superuser_email_non_existant(self):
        with self.assertRaises(ValueError):
            user = UserFactory.create_superuser(email=None, password='test')
        self.assertEqual(len(User.objects.all()), 0)

    def test_create_superuser_is_not_superuser(self):
        with self.assertRaises(ValueError):
            user = UserFactory.create_superuser(email='test@test.com', password='test', is_superuser=False)
        self.assertEqual(len(User.objects.all()), 0)

    # User Views
    def test_user_list_view_exists(self):
        view = UserListCreateView.as_view()

        response = self.client.get(reverse('user-list-create'))

        self.assertEqual(response.status_code, 200)

    def test_user_list_view_not_authenticated(self):
        user1 = UserFactory.create(email='test1@test.com')
        user2 = UserFactory.create_superuser(email='test2@test.com', password='test')

        view = UserListCreateView.as_view()

        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('user-list-create'))

        self.assertEqual(len(response.data['results']), 0)

    def test_user_list_view_authenticated_as_user(self):
        user1 = UserFactory.create(email='test1@test.com')
        user2 = UserFactory.create_superuser(email='test2@test.com', password='test')

        view = UserListCreateView.as_view()

        self.client.force_authenticate(user=user1)
        response = self.client.get(reverse('user-list-create'))

        self.assertEqual(len(response.data['results']), 1)
        # TODO make sure content is correct

    def test_user_list_view_authenticated_as_superuser(self):
        user1 = UserFactory.create(email='test1@test.com')
        user2 = UserFactory.create_superuser(email='test2@test.com', password='test')

        view = UserListCreateView.as_view()

        self.client.force_authenticate(user=user2)
        response = self.client.get(reverse('user-list-create'))

        self.assertEqual(len(response.data['results']), 2)
        # TODO make sure content is correct

    def test_user_list_create_success(self):
        view = UserListCreateView.as_view()

        response = self.client.post(reverse('user-list-create'), {
                'name': 'test',
                'birth_date': '1900-01-01',
                'email': 'test@test.com',
                'password': 'test',
            }, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(len(User.objects.all()), 0)

    def test_user_list_create_invalid_data(self):
        view = UserListCreateView.as_view()

        response = self.client.post(reverse('user-list-create'), {
                'name': None,
                'birth_date': None,
                'email': None,
                'password': None,
            }, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(User.objects.all()), 0)

    def test_user_view_not_authenticated(self):
        view = UserRetrieveUpdateDestroyView.as_view()

        user = UserFactory.create()

        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('user-retrieve-update-destroy', kwargs={"user_id": user.id}))

        self.assertEqual(response.status_code, 404)

    def test_user_view_authenticated_as_user_self(self):
        view = UserRetrieveUpdateDestroyView.as_view()

        user = UserFactory.create()

        self.client.force_authenticate(user=user)
        response = self.client.get(reverse('user-retrieve-update-destroy', kwargs={"user_id": user.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], user.id)

    def test_user_view_authenticated_as_user_other(self):
        view = UserRetrieveUpdateDestroyView.as_view()

        user1 = UserFactory.create(email='test1@test.com')
        user2 = UserFactory.create(email='test2@test.com')

        self.client.force_authenticate(user=user1)
        response = self.client.get(reverse('user-retrieve-update-destroy', kwargs={"user_id": user2.id}))

        self.assertEqual(response.status_code, 404)

    def test_user_view_authenticated_as_superuser(self):
        view = UserRetrieveUpdateDestroyView.as_view()

        user1 = UserFactory.create_superuser(email='test1@test.com', password='test')
        user2 = UserFactory.create(email='test2@test.com')

        self.client.force_authenticate(user=user1)
        response = self.client.get(reverse('user-retrieve-update-destroy', kwargs={"user_id": user2.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], user2.id)

    def test_user_update_invalid_data(self):
        view = UserRetrieveUpdateDestroyView.as_view()

        user = UserFactory.create_superuser(name='test', email='test@test.com', password='test')

        self.client.force_authenticate(user=user)
        response = self.client.put(reverse('user-retrieve-update-destroy', kwargs={"user_id": user.id}), {
                "id": user.id,
                "name": None,
                "birth_date": user.birth_date,
                "email": user.email,
                "password": user.password,
            }, format='json')

        self.assertEqual(response.status_code, 400)

        user_new = User.objects.get(id=user.id)
        self.assertEqual(user_new.name, "test")

    def test_user_update_not_authenticated(self):
        view = UserRetrieveUpdateDestroyView.as_view()

        user = UserFactory.create()

        self.client.force_authenticate(user=None)
        response = self.client.put(reverse('user-retrieve-update-destroy', kwargs={"user_id": user.id}), {
                "id": user.id,
                "name": "test2",
                "birth_date": user.birth_date,
                "email": user.email,
                "password": user.password,
            }, format='json')

        self.assertEqual(response.status_code, 404)

        user_new = User.objects.get(id=user.id)
        self.assertEqual(user_new.name, "test")

    def test_user_update_authenticated_as_user_self(self):
        view = UserRetrieveUpdateDestroyView.as_view()

        user = UserFactory.create()

        self.client.force_authenticate(user=user)
        response = self.client.put(reverse('user-retrieve-update-destroy', kwargs={"user_id": user.id}), {
                "id": user.id,
                "name": "test2",
                "birth_date": user.birth_date,
                "email": user.email,
                "password": user.password,
            }, format='json')

        self.assertEqual(response.status_code, 200)

        user_new = User.objects.get(id=user.id)
        self.assertEqual(user_new.name, "test2")

    def test_user_update_authenticated_as_user_other(self):
        view = UserRetrieveUpdateDestroyView.as_view()

        user1 = UserFactory.create(email="test1@test.com")
        user2 = UserFactory.create(email="test2@test.com")

        self.client.force_authenticate(user=user1)
        response = self.client.put(reverse('user-retrieve-update-destroy', kwargs={"user_id": user2.id}), {
                "id": user2.id,
                "name": "test2",
                "birth_date": user2.birth_date,
                "email": user2.email,
                "password": user2.password,
            }, format='json')

        self.assertEqual(response.status_code, 404)

        user_new = User.objects.get(id=user2.id)
        self.assertEqual(user_new.name, "test")

    def test_user_update_authenticated_as_superuser(self):
        view = UserRetrieveUpdateDestroyView.as_view()

        user1 = UserFactory.create_superuser(email="test1@test.com", password="test")
        user2 = UserFactory.create(email="test2@test.com")

        self.client.force_authenticate(user=user1)
        response = self.client.put(reverse('user-retrieve-update-destroy', kwargs={"user_id": user2.id}), {
                "id": user2.id,
                "name": "test2",
                "birth_date": user2.birth_date,
                "email": user2.email,
                "password": user2.password,
            }, format='json')

        self.assertEqual(response.status_code, 200)

        user_new = User.objects.get(id=user2.id)
        self.assertEqual(user_new.name, "test2")

    def test_user_destroy_not_authenticated(self):
        view = UserRetrieveUpdateDestroyView.as_view()

        user = UserFactory.create()

        self.client.force_authenticate(user=None)
        response = self.client.delete(reverse('user-retrieve-update-destroy', kwargs={"user_id": user.id}))

        self.assertEqual(response.status_code, 404)

        try:
            user_new = User.objects.get(id=user.id)
        except User.DoesNotExist:
            self.fail("DoesNotExist raised")

    def test_user_destroy_authenticated_as_user_self(self):
        view = UserRetrieveUpdateDestroyView.as_view()

        user = UserFactory.create()

        self.client.force_authenticate(user=user)
        response = self.client.delete(reverse('user-retrieve-update-destroy', kwargs={"user_id": user.id}))

        self.assertEqual(response.status_code, 403)

        try:
            user_new = User.objects.get(id=user.id)
        except User.DoesNotExist:
            self.fail("DoesNotExist raised")

    def test_user_destroy_authenticated_as_user_other(self):
        view = UserRetrieveUpdateDestroyView.as_view()

        user1 = UserFactory.create(email="test1@test.com")
        user2 = UserFactory.create(email="test2@test.com")

        self.client.force_authenticate(user=user1)
        response = self.client.delete(reverse('user-retrieve-update-destroy', kwargs={"user_id": user2.id}))

        self.assertEqual(response.status_code, 404)

        try:
            user2_new = User.objects.get(id=user2.id)
        except User.DoesNotExist:
            self.fail("DoesNotExist raised")

    def test_user_destroy_authenticated_as_superuser(self):
        view = UserRetrieveUpdateDestroyView.as_view()

        user1 = UserFactory.create_superuser(email="test1@test.com", password="test")
        user2 = UserFactory.create(email="test2@test.com")

        self.client.force_authenticate(user=user1)
        response = self.client.delete(reverse('user-retrieve-update-destroy', kwargs={"user_id": user2.id}))

        self.assertEqual(response.status_code, 204)

        with self.assertRaises(User.DoesNotExist):
            user2_new = User.objects.get(id=user2.id)
