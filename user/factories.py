from factory import Factory

from user.models import User


class UserFactory(Factory):

    class Meta:
        model = User

    email = 'test@test.com'
    name = 'test'
    password = 'test'

    def _get_manager():
        return User.objects

    @classmethod
    def _create(self, model_class, *args, **kwargs):
        kwargs['username'] = kwargs['email']
        return self._get_manager().create_user(*args, **kwargs)

    @classmethod
    def create_superuser(self, username, email, password, **extra_fields):
        return self._get_manager().create_superuser(
            username, email, password, **extra_fields)
