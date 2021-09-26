from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from users_api.models import User


class Tag(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)
    color = models.CharField(max_length=7, null=False, blank=False, unique=True, validators=[RegexValidator('#[0-9A-F]{6}$', 'Color code must be in hex format, i.e. \'#FFFFFF\'')])
    slug = models.SlugField(max_length=200, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return self.name + ' (' + self.measurement_unit + ')'


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False)
    ingredients = models.ManyToManyField(Ingredient, through='Portion', blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    image = models.URLField(null=False, blank=False)
    text = models.TextField(null=False, blank=False)
    cooking_time = models.IntegerField(
        null=False, blank=False, validators=[MinValueValidator(1), ])

    def __str__(self):
        return self.name

class Portion(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return self.recipe.name + ' <<< ' + self.ingredient.name

class Favorite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe, blank=True)

    def __str__(self):
        return self.user.username + ' >>> ' + str(self.recipes.all())

class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe, blank=True)

    def __str__(self):
        return self.user.username +  ' >>> ' + str(self.recipes.all())