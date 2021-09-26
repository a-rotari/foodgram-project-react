from django.contrib import admin
from .models import Tag, Ingredient, Recipe, Portion, Favorite, ShoppingCart

class PortionInLine(admin.TabularInline):
    model = Portion
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inlines = (PortionInLine,)

class IngredientAdmin(admin.ModelAdmin):
    inlines = (PortionInLine,)

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Portion)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)