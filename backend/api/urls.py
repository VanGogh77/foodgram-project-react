from django.urls import path, include
from rest_framework import routers

from api.views import (
    UserViewSet, TagViewSet,
    IngredientViewSet, RecipeViewSet,
)

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('tags', TagViewSet, basename='tag')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('v1/auth/', include('djoser.urls.authtoken')),
]
