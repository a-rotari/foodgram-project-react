from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'tags', views.TagViewSet)
router.register(r'ingredients', views.IngredientViewSet)
router.register(r'recipes', views.RecipeViewSet)

urlpatterns = [
    path('recipes/download_shopping_cart/',
         views.DownloadShoppingCart.as_view(), name='download-shopping-cart'),
    path('recipes/<int:pk>/favorite/',
         views.AddRemoveFavorite.as_view(), name='add-remove-favorite'),
    path('recipes/<int:pk>/shopping_cart/',
         views.AddRemoveShoppingCart.as_view(), name='add-remove-shopping-cart'),
    path('', include(router.urls)),
]
