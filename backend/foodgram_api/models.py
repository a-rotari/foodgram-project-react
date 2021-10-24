from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from users_api.models import User


class Tag(models.Model):
    """ Model for Tag objects. """
    name = models.CharField(max_length=200, unique=True)
    # "давай попробуем уберечь пользователя от необходимости вводить хекс-код"
    # Прости, но непонятно. По ТЗ же hex-код должен быть.
    color = models.CharField(
        max_length=7, unique=True, validators=[RegexValidator(
            '#[0-9A-F]{6}$',
            'Color code must be in hex format, i.e. \'#FFFFFF\'')])
    # Максимальная длина слага 200 согласно документации (<= 200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        # ordering = ['name']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """ Model for Ingredient objects. """
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        # ordering = ['name']

    def __str__(self):
        return self.name + ' (' + self.measurement_unit + ')'


class Recipe(models.Model):
    """ Model for Recipe objects. """
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(
        Ingredient, through='Portion')
    name = models.CharField(max_length=200)
    image = models.FileField()
    text = models.TextField()
    cooking_time = models.IntegerField(validators=[MinValueValidator(
        1, message='Время приготовления не может быть меньше минуты.'), ])

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        # ordering = ['name']

    def __str__(self):
        return self.name


class Portion(models.Model):
    """
    Intermediate model enabling additional 'amount' field
    in the many-to-many relation between Recipe and Ingredient.
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(
        0, message='Количество ингредиентов не может быть отрицательным.'), ])

    class Meta:
        verbose_name = 'Ingredient in a Recipe'
        verbose_name_plural = 'Ingredients in Recipes'
        # ordering = ['recipe']
        unique_together = ['recipe', 'ingredient']

    def __str__(self):
        return self.recipe.name + ' <<< ' + self.ingredient.name


class Favorite(models.Model):
    """
    Intermediate model functioning as an additional field on User model and
    enabling many-to-many relations between User and Recipe.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe, blank=True)

    class Meta:
        verbose_name = 'User\'s favorite Recipe'
        verbose_name_plural = 'Users\' favorite Recipes'
        # ordering = ['user']

    def __str__(self):
        return self.user.username + ' >>> ' + str(self.recipes.all())


class ShoppingCart(models.Model):
    """
    Intermediate model functioning as an additional field on User model and
    enabling many-to-many relations between User and Recipe.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe, blank=True)

    class Meta:
        verbose_name = 'Recipe in Shopping Cart'
        verbose_name_plural = 'Recipes in Shopping Carts'
        # ordering = ['user']

    def __str__(self):
        return self.user.username + ' >>> ' + str(self.recipes.all())
