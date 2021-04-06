from django.contrib import admin
from .models import (
    GameClan,
    GameClanUser,
    GameClanChat, GameChatMessage,

)


@admin.register(GameClan)
class GameClanAdmin(admin.ModelAdmin):
    pass


@admin.register(GameClanUser)
class GameClanUserAdmin(admin.ModelAdmin):
    list_display = ['clan', 'user']


@admin.register(GameClanChat)
class GameClanChatAdmin(admin.ModelAdmin):
    pass


@admin.register(GameChatMessage)
class GameChatMessageAdmin(admin.ModelAdmin):
    pass
