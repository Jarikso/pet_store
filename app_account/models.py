from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    USERNAME_FIELD = 'email'  # переопределят модель для входа в аккаунт
    REQUIRED_FIELDS = ['username']
    full_name = models.CharField(max_length=50, db_index=True, verbose_name='полное имя')
    avatar = models.ImageField(upload_to='img_profile/', blank=True, verbose_name='изображение')
    phone = PhoneNumberField(null=True, blank=True, unique=True, verbose_name='телефон')
    email = models.EmailField(_('email address'), unique=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = f'person_{len(User.objects.all()) + 1}'
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('account:change', kwargs={'pk': self.id})
