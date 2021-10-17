from django.db import models
from django_filters import rest_framework as filters

from .models import Recipe, Tag


class RecipeFilter(filters.FilterSet):
    author = filters.NumberFilter(field_name='author__id')
    is_favorited = filters.NumberFilter(method='filter_favorited')
    is_in_shopping_cart = filters.NumberFilter(method='filter_shopping_cart')
    tags = filters.CharFilter(method='filter_tags')

    def filter_queryset(self, queryset):
        """ Overriding django-filter parent class method to combine the
            results of filtering using several query parameters """
        for name, value in self.form.cleaned_data.items():
            filtered_queryset = self.filters[name].filter(queryset, value)
            queryset = queryset.intersection(filtered_queryset)
            assert isinstance(queryset, models.QuerySet), \
                "Expected '%s.%s' to return a QuerySet, but got a %s instead." \
                % (type(self).__name__, name, type(queryset).__name__)
        return queryset

    def filter_favorited(self, queryset, name, value):
        if value == 1 and self.request.user.is_authenticated:
            queryset = self.request.user.favorite.recipes.all()
        return queryset

    def filter_shopping_cart(self, queryset, name, value):
        if value == 1 and self.request.user.is_authenticated:
            queryset = self.request.user.shoppingcart.recipes.all()
        return queryset

    def filter_tags(self, queryset, name, value):
        if name:
            tag_slugs = self.request.query_params.getlist('tags')
            tag_id = []
            for tag_slug in tag_slugs:
                tag_id.append(Tag.objects.get(slug=tag_slug).id)
            queryset = Recipe.objects.filter(tags__in=tag_id)
        return queryset

    class Meta:
        model = Recipe
        fields = ['author', 'tags']
