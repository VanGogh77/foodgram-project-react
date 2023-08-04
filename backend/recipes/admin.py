from django.contrib import admin

from recipes.models import (
    Tag, Recipes,
    Ingredient, Recipe_page,
    Shopping_list, Favorites
)


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'units')
    search_fields = ('name',)
    list_filter = ('name',)


class RecipesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'name', 'in_favorites')
    list_editable = ('author', 'name', 'image', 'text',
        'image', 'cooking_time'
)
    readonly_fields = ('in_favorites',)
    list_filter = ('author', 'name', 'tag')
    empty_value_display = '-пусто-'
    def in_favorites(self, obj):
        return obj.favorite_recipe.count()


class RecipePageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient')
    list_editable = ('recipe', 'ingredient')


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_editable = ('user', 'recipe')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_editable = ('user', 'recipe')


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipes)
admin.site.register(Recipe_page)
admin.site.register(Shopping_list)
admin.site.register(Favorites)