from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


def emailvalidator(value: str):
    if 'rambler.ru' in value:
        raise ValidationError("Запрещена регистрация с почтового адреса в домене rambler.ru")


def minlenvalueslug(value: str):
    if len(value) < 5:
        raise ValidationError('Значение длины слага не может быть меньше 5')


def name_validator(value: str):
    if len(value) < 10:
        raise ValidationError('Минимальная длина имени должна быть не меньше 10 символам')


def is_published_validator(value: bool):
    if value:
        raise ValidationError(
            'Значение поля is_published на момент создания не должно равняться True, по умолчанию стоит False')


class Locations(models.Model):
    name = models.TextField()
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.TextField()
    slug = models.CharField(null=True, max_length=10, unique=True, validators=[minlenvalueslug])

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Users(AbstractUser):
    ADMIN = "admin"
    M0DERATOR = "moderator"
    USER = "user"
    ROLE = [(M0DERATOR, "moderator"), (ADMIN, "admin"), (USER, "user")]
    role = models.CharField(max_length=9, choices=ROLE, default=USER)
    age = models.IntegerField()
    location = models.ManyToManyField('Locations')
    last_name = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True)
    email = models.EmailField(null=True, blank=True, unique=True, validators=[emailvalidator])

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return self.username


class Ads(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, validators=[name_validator])
    author = models.ForeignKey('Users', on_delete=models.CASCADE)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.TextField(null=True, blank=True)
    is_published = models.BooleanField(default=False, validators=[is_published_validator])
    logo = models.ImageField(upload_to='logos/')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

        def __str__(self):
            return self.name


class Compilation(models.Model):
    name = models.CharField(max_length=100)
    items = models.ManyToManyField('Ads')
    owner = models.ForeignKey('Users', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'
