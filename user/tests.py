# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from factory import Factory

from django.test import TestCase
from django.test import Client
from rest_framework.test import APIRequestFactory, force_authenticate

from .views import UserListCreateView
from .models import UserManager, User

# Create your tests here.

class UserFactory(Factory):
    class Meta:
        model = User

    email = 'test@test.com'
    name = 'Test'
    password = 'test'

    def _get_manager():
        return User.objects

    @classmethod
    def _create(self, model_class, *args, **kwargs):
        return self._get_manager().create_user(*args, **kwargs)

    @classmethod
    def create_superuser(self, email, password, **extra_fields):
        return self._get_manager().create_superuser(email, password, **extra_fields)

class UserTests(TestCase):

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

    # Views
    def test_user_list_view_exists(self):
        factory = APIRequestFactory()
        view = UserListCreateView.as_view()

        request = factory.get('/api/v1/users/')
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_user_list_view_not_authenticated(self):
        user1 = UserFactory.create(email='test1@test.com')
        user2 = UserFactory.create_superuser(email='test2@test.com', password='test')

        factory = APIRequestFactory()
        view = UserListCreateView.as_view()

        request = factory.get('/api/v1/users/')
        force_authenticate(request, user=None)
        response = view(request)

        self.assertEqual(len(response.data), 0)

    def test_user_list_view_authenticated_as_user(self):
        user1 = UserFactory.create(email='test1@test.com')
        user2 = UserFactory.create_superuser(email='test2@test.com', password='test')

        factory = APIRequestFactory()
        view = UserListCreateView.as_view()

        request = factory.get('/api/v1/users/')
        force_authenticate(request, user=user1)
        response = view(request)

        self.assertEqual(len(response.data), 1)
        # TODO make sure content is correct

    def test_user_list_view_authenticated_as_superuser(self):
        user1 = UserFactory.create(email='test1@test.com')
        user2 = UserFactory.create_superuser(email='test2@test.com', password='test')

        factory = APIRequestFactory()
        view = UserListCreateView.as_view()

        request = factory.get('/api/v1/users/')
        force_authenticate(request, user=user2)
        response = view(request)

        self.assertEqual(len(response.data), 2)
        # TODO make sure content is correct

    def test_user_list_create_success(self):
        factory = APIRequestFactory()
        view = UserListCreateView.as_view()

        request = factory.post('/api/v1/users/', {
                'name': 'test',
                'birth_date': '1900-01-01',
                'email': 'test@test.com',
                'password': 'test',
            }, format='json')

        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(len(User.objects.all()), 0)

    def test_user_list_create_invalid_data(self):
        factory = APIRequestFactory()
        view = UserListCreateView.as_view()

        request = factory.post('/api/v1/users/', {
                'name': None,
                'birth_date': None,
                'email': None,
                'password': None,
            }, format='json')

        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(User.objects.all()), 0)

    def test_user_update_success(self):
        factory = APIRequestFactory()
        view = UserListCreateView.as_view()

        user = UserFactory.create()

        request = factory.put('/api/v1/users/' + str(user.id) + '/', {
                "id": user.id,
                "name": "test2",
                "birth_date": user.birth_date,
                "email": user.email,
                "password": user.password,
            }, format='json')
        force_authenticate(request, user=user)

        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.name, "test2")
