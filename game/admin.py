from django.contrib import admin
from django.db import models
from django.forms import Textarea, ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    Game,
    GameClan,
    GameClanUser,
    GameClanChat, GameChatMessage,

)


def _link_to(objects, admin_name, args, name):
    url = reverse(f'admin:{admin_name}', args=[args])
    link = f'<a href={url}>{name}</a>'
    return mark_safe(link)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['game', 'slug']


@admin.register(GameClanUser)
class GameClanUserAdmin(admin.ModelAdmin):
    list_display = ['clan_user', 'clan_link', 'user_link', ]

    @staticmethod
    def clan_user(objects):
        return objects.user

    @staticmethod
    def clan_link(objects):
        return _link_to(objects, 'game_gameclan_change', objects.clan_id, objects.clan)

    @staticmethod
    def user_link(objects):
        return _link_to(objects, 'auth_user_change', objects.user.id, objects.user)


class ClanUsersInline(admin.TabularInline):
    model = GameClanUser
    extra = 1
    classes = ('collapse',)

    fields = ('user', 'clan_user_link', 'user_link',)
    readonly_fields = ('clan_user_link', 'user_link',)

    def clan_user_link(self, object):
        return _link_to(object, 'game_gameclanuser_change', object.user.id, object.user)

    def user_link(self, object):
        return _link_to(object, 'auth_user_change', object.user.id, object.user)


class ClanChatInline(admin.TabularInline):
    model = GameClanChat
    extra = 0
    classes = ('collapse',)



@admin.register(GameClan)
class GameClanAdmin(admin.ModelAdmin):
    list_display = ('name', 'game_link', 'created_at',)
    fieldsets = (
        ('Clan', {
            'fields': ('game', 'name', 'description', 'creator', 'max_users',)
        }),
    )
    search_fields = ('name',)
    list_display_links = ('name',)
    list_filter = ('game',)
    inlines = [
        ClanChatInline,
        ClanUsersInline,
    ]

    @staticmethod
    def game_link(objects):
        return _link_to(objects, 'game_game_change', objects.game_id, objects.game.game)


class MsgInline(admin.TabularInline):
    model = GameChatMessage
    extra = 1
    classes = ('collapse',)
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(
                attrs={
                    'rows': 1,
                    'cols': 40,
                    'style': 'height: 1em;'
                }
            )
        }
    }


@admin.register(GameClanChat)
class GameClanChatAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'clan_link', 'game')
    inlines = [MsgInline, ]

    @staticmethod
    def clan_link(objects):
        return _link_to(objects, 'game_gameclan_change', objects.clan_id, objects.clan)

    @staticmethod
    def game(objects):
        return objects.clan.game


@admin.register(GameChatMessage)
class GameChatMessageAdmin(admin.ModelAdmin):
    list_display = ('type', 'clan_chat', 'clan_user_link', 'msg', 'created_at')
    list_filter = ('clan_chat', 'clan_chat__clan__game')

    def msg(self, objects):
        text = objects.text
        return text[:min(len(text), 20)] + '...'

    @staticmethod
    def clan_user_link(objects):
        return _link_to(objects, 'game_gameclanuser_change', objects.user.id, objects.user)
