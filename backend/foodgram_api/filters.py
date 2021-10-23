from django.db import models
from django_filters import rest_framework as filters

from .models import Recipe, Tag


class RecipeFilter(filters.FilterSet):
    """
    Custom filterset for the view handling Recipe operations.
    Filtering criteria: Recipe author, whether the Recipe is in Favorite,
    whether Recipe is in ShoppingCart, Recipe tags.
    """
    author = filters.NumberFilter(field_name='author__id')
    is_favorited = filters.BooleanFilter(method='filter_favorited')
    is_in_shopping_cart = filters.BooleanFilter(method='filter_shopping_cart')
    tags = filters.CharFilter(method='filter_tags')

    def filter_queryset(self, queryset):
        """ Overriding django-filter parent class method to combine the
            results of filtering using several query parameters """
        for name, value in self.form.cleaned_data.items():
            filtered_queryset = self.filters[name].filter(queryset, value)
            queryset = queryset.intersection(filtered_queryset)
        return queryset

    def filter_favorited(self, queryset, name, value):
        if (value is True) and self.request.user.is_authenticated:
            return self.request.user.favorite.recipes.all()
        return queryset

    def filter_shopping_cart(self, queryset, name, value):
        if (value is True) and self.request.user.is_authenticated:
            return self.request.user.shoppingcart.recipes.all()
        return queryset

    def filter_tags(self, queryset, name, value):
        if name:
            tag_slugs = self.request.query_params.getlist('tags')
            tag_id = []
            for tag_slug in tag_slugs:
                tag_id.append(Tag.objects.get(slug=tag_slug).id)
            return Recipe.objects.filter(tags__in=tag_id)
        return queryset

    class Meta:
        model = Recipe
        fields = ['author', 'tags']
