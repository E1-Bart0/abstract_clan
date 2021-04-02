from django.contrib import admin
from .models import (
    GameClan,
    GameClanUser,
    GameClanChat,
    GameClanInfo,
    GameClanSettings
)


@admin.register(GameClan)
class GameClanAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_info', 'settings', 'clan_users',)

    def clan_users(self, obj):
        return '\n'.join(user.user.username for user in obj.get_users)

    def get_info(self, obj):
        return obj.info


@admin.register(GameClanUser)
class GameClanUserAdmin(admin.ModelAdmin):
    list_display = ['clan', 'user']


@admin.register(GameClanChat)
class GameClanChatAdmin(admin.ModelAdmin):
    list_display = ['clan', 'user', 'text', 'pub_date']


@admin.register(GameClanInfo)
class GameClanInfoAdmin(admin.ModelAdmin):
    list_display = ('description', 'rating')


@admin.register(GameClanSettings)
class GameClanSettingsAdmin(admin.ModelAdmin):
    list_display = ['open_close', 'min_rating', 'created_at']
