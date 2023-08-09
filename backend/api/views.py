from http import HTTPStatus
from django.shortcuts import render
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, generics, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from .pagination import CustomPaginator

from foodgram_backend.settings import FILE_NAME
from users.models import Subscribe, User
from recipes.models import Tag, Ingredient, Recipes, Favorites, Shopping_list
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
    permission_classes = [AllowAny]
    serializer_class = UserListSerializer
    pagination_class = CustomPaginator

    @action(
        methods=[
            'GET',
            'PATCH',
        ],
        permission_classes=[IsAuthenticated],
        detail=False,
        url_path='me',
    )
    def users_profile(self, request):
        serializer = UserListSerializer(request.user)
        return Response(serializer.data, status=HTTPStatus.OK)
    
    @action(
        methods=['POST'],
        permission_classes=[IsAuthenticated],
        detail=False,
    )
    def users_password(self, request):
        serializer = ChangePasswordSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Пароль изменен!'}, status=HTTPStatus.NO_CONTENT)
        
    @action(
        methods=['GET'],
        permission_classes =[IsAuthenticated],
        detail=False,
        pagination_class = CustomPaginator
    )
    def subscriptions(self, request):
        serializer = SubscribesSerializer(request.user)
        return self.get_paginated_response(serializer.data)
    
    @action(
        methods=[
            'POST',
            'DELETE',
        ],
        permission_classes =[IsAuthenticated],
        detail=False,
    )
    def subsscribe(self, request, **kwargs):
        author = get_object_or_404(User, id=kwargs['pk'])

        if request.method == 'POST':
            serializer = SubscribeAuthorSerializer(
                author, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            Subscribe.objects.create(user=request.user, author=author)
            return Response(serializer.data, status=HTTPStatus.CREATED)

        if request.method == 'DELETE':
            get_object_or_404(Subscribe, user=request.user,
                              author=author).delete()
            return Response({'detail': 'Удалено'},
                            status=HTTPStatus.NO_CONTENT)


class TagViewSet(mixins.ListModelMixin,
          mixins.RetrieveModelMixin,
          viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


class IngredientViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    search_fields = ('^name', )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPaginator
    http_method_names = ['get', 'post', 'patch', 'create', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateSerializer
    
    @action(
        methods=[
            'POST',
            'DELETE',
        ],
        permission_classes=[IsAuthenticated],
        detail=True
    )
    def favorites(self, request, **kwargs):
        recipe = get_object_or_404(Recipes, id=kwargs['pk'])

        if request.method == 'POST':
            serializer = RecipeSerializer(recipe, data=request.data,
                                          context={"request": request})
            serializer.is_valid(raise_exception=True)
            if not Favorites.objects.filter(user=request.user,
                                           recipe=recipe).exists():
                Favorites.objects.create(user=request.user, recipe=recipe)
                return Response(serializer.data,
                                status=HTTPStatus.CREATED)
            return Response({'errors': 'Рецепт уже в избранном.'},
                            status=HTTPStatus.BAD_REQUEST)

        if request.method == 'DELETE':
            get_object_or_404(Favorites, user=request.user,
                              recipe=recipe).delete()
            return Response({'detail': 'Рецепт успешно удален из избранного.'},
                            status=HTTPStatus.NO_CONTENT)
        
    @action(
        methods=[
            'POST',
            'DELETE',
        ],
        permission_classes=[IsAuthenticated],
        detail=True
    )
    def shopping_list(self, request, **kwargs):
        recipe = get_object_or_404(Recipes, id=kwargs['pk'])

        if request.method == 'POST':
            serializer = RecipeSerializer(recipe, data=request.data,
                                          context={"request": request})
            serializer.is_valid(raise_exception=True)
            if not Shopping_list.objects.filter(user=request.user,
                                                recipe=recipe).exists():
                Shopping_list.objects.create(user=request.user, recipe=recipe)
                return Response(serializer.data,
                                status=HTTPStatus.CREATED)
            return Response({'errors': 'Рецепт уже в списке покупок.'},
                            status=HTTPStatus.BAD_REQUEST)

        if request.method == 'DELETE':
            get_object_or_404(Shopping_list, user=request.user,
                              recipe=recipe).delete()
            return Response(
                {'detail': 'Рецепт успешно удален из списка покупок.'},
                status=HTTPStatus.NO_CONTENT)
        
    @action(
        methods=['GET'],
        permission_classes=[IsAuthenticated],
        detail=True
    )
    def download_shopping_list(self, request, **kwargs):
        ingredients = (
            Recipes.objects
            .filter(recipe__shopping_recipe__user=request.user)
            .values('ingredient')
            .annotate(total_amount=Sum('amount'))
            .values_list('ingredient__name', 'total_amount',
                         'ingredient__measurement_unit')
        )
        file_list = []
        [file_list.append(
            '{} - {} {}.'.format(*ingredient)) for ingredient in ingredients]
        file = HttpResponse('Cписок покупок:\n' + '\n'.join(file_list),
                            content_type='text/plain')
        file['Content-Disposition'] = (f'attachment; filename={FILE_NAME}')
        return file
