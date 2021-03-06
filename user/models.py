from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from utils import files


class UserManager(BaseUserManager):
    use_in_migrations = True

    def get_by_natural_key(self, username):
        return self.get(username=username)

    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The given email must be set')

        if not username:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('other', 'Other'),
        ('male', 'Male'),
        ('female', 'Female'),
    )

    username = models.CharField(_('username'), unique=True, max_length=50)
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'), max_length=50, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('is staff'), default=False)
    birth_date = models.DateField(blank=True, null=True)

    picture = models.ImageField(
        upload_to=files.s3_upload_path('users', username, 'picture'),
        default='users/picture/anonymous.jpg')

    gender = models.CharField(
        _('gender'),
        choices=GENDER_CHOICES,
        max_length=16,
        default="other")

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ['id']
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        return self.name.strip()

    def get_short_name(self):
        return self.get_full_name()
