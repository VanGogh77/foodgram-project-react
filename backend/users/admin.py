from django.contrib import admin

from users.models import User, Subscribe


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'pk',
        'email',
    )
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user')
    list_editable = ['user']
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)