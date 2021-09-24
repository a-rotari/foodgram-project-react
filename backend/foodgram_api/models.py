from django.db import models
from django.core.validators import MinValueValidator
from users_api.models import User


class Tag(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    color = models.CharField(max_length=7, null=True)
    slug = models.SlugField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    measurement_unit = models.CharField(max_length=200)
    amount = models.IntegerField(null=True, validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False)
    ingredients = models.ManyToManyField(Ingredient)
    name = models.CharField(max_length=200, null=False, blank=False)
    image = models.URLField(null=False, blank=False)
    text = models.TextField(null=False, blank=False)
    cooking_time = models.IntegerField(
        null=False, blank=False, validators=[MinValueValidator(1), ])
