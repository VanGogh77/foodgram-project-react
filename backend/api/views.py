from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, generics, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import Subscribe, User
from .permissions import IsOwnerOrReadOnly
from .pagination import CustomPaginator
from .serializers import (
    UserListSerializer, SignUpSerializer, ChangePasswordSerializer,
    RecipeSerializer, SubscribesSerializer, SubscribeAuthorSerializer,
    TagSerializer, IngredientSerializer, RecipeIngredientSerializer,
    RecipePageSerializer, RecipeIngredientCreateSerializer,
    RecipeCreateSerializer
)


class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                  mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
