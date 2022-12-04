from django.db import models
from django.contrib.auth.models import AbstractUser


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

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return self.username


class Ads(models.Model):
    name = models.TextField()
    author = models.ForeignKey('Users', on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField()
    is_published = models.BooleanField(default=False)
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
