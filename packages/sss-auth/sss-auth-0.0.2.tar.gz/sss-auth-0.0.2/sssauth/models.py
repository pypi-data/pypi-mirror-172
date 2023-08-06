from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator, RegexValidator

class MyUserManager(BaseUserManager):
    def create_user(self, address, email):
        if not address:
            raise ValueError('Users must have an Address')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            address=address,
            email=self.normalize_email(email),
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, address, email):
        user = self.create_user(
            address=address,
            email=self.normalize_email(email),
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser, PermissionsMixin):

    address = models.CharField(verbose_name='address', max_length=45, unique=True, validators=[MinLengthValidator(39,), RegexValidator(r'^[a-zA-Z0-9]*$',)])
    email = models.EmailField(verbose_name='email', max_length=50, unique=True)
    date_joined = models.DateTimeField(verbose_name='joined', auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()
    # identify
    USERNAME_FIELD = 'address'
    # list
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.address