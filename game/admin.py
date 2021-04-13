from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.forms import Textarea
from django.urls import reverse
from django.utils.safestring import mark_safe

from myuser.models import User
from .apps import GameConfig
from .models import (
    Game,
    GameClan,
    GameClanMember,
    GameClanChat,
    GameChatTextMessage,
    GameChatRequestItem,
    GameChatRequestResource, GameChatNotification,
)

admin.site.register(User, UserAdmin)

BASEDIR = GameConfig.name
ADMIN_URL = lambda path: BASEDIR + '_' + BASEDIR + path + '_change'


def _link_to(admin_name, args, name):
    url = reverse(f'admin:{admin_name}', args=[args])
    link = f'<a href={url}>{name}</a>'
    return mark_safe(link)


class ClanMembersInline(admin.TabularInline):
    model = GameClanMember
    extra = 1
    classes = ('collapse',)

    fields = ('user', 'clan_member_link', 'user_link',)
    readonly_fields = ('clan_member_link', 'user_link',)

    def clan_member_link(self, object):
        return _link_to(ADMIN_URL('clanmember'), object.user.id, object.user)

    def user_link(self, object):
        return _link_to('myuser_user_change', object.user.id, object.user)


class ClanChatsInline(admin.TabularInline):
    model = GameClanChat
    extra = 0
    classes = ('collapse',)


class MessagesInline(admin.TabularInline):
    model = GameChatTextMessage
    extra = 0
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


class ResourceRequestInline(admin.TabularInline):
    model = GameChatRequestResource
    extra = 0
    classes = ('collapse',)


class ItemsRequestInline(admin.TabularInline):
    model = GameChatRequestItem
    extra = 0
    classes = ('collapse',)


class NotificationsInline(admin.TabularInline):
    model = GameChatNotification
    extra = 0
    classes = ('collapse',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['game', 'slug']


@admin.register(GameClanMember)
class GameClanMembersAdmin(admin.ModelAdmin):
    list_display = ['clan_member', 'clan_link', 'user_link', ]

    @staticmethod
    def clan_member(objects):
        return objects.user

    @staticmethod
    def clan_link(objects):
        return _link_to(ADMIN_URL('clan'), objects.clan_id, objects.clan)

    @staticmethod
    def user_link(objects):
        return _link_to('myuser_user_change', objects.user.id, objects.user)


@admin.register(GameClan)
class GameClanAdmin(admin.ModelAdmin):
    list_display = ('name', 'game_link', 'created_at', 'creator')
    fieldsets = (
        ('Clan', {
            'fields': ('game', 'name', 'description', 'creator', 'max_members',)
        }),
    )
    search_fields = ('name',)
    list_display_links = ('name',)
    list_filter = ('game',)
    inlines = [
        ClanChatsInline,
        ClanMembersInline,
    ]

    @staticmethod
    def game_link(objects):
        return _link_to(ADMIN_URL(''), objects.game_id, objects.game.game)


@admin.register(GameClanChat)
class GameClanChatAdmin(admin.ModelAdmin):
    list_display = ('name', 'clan_link', 'game')
    inlines = [
        MessagesInline,
        ResourceRequestInline,
        ItemsRequestInline,
        NotificationsInline,
    ]
    list_filter = ('clan__game', 'clan',)

    @staticmethod
    def clan_link(objects):
        return _link_to(ADMIN_URL('clan'), objects.clan_id, objects.clan)

    @staticmethod
    def game(objects):
        return objects.clan.game

# @admin.register(GameChatTextMessage)
# class GameChatMessageAdmin(admin.ModelAdmin):
#     list_display = ('type', 'clan_chat', 'clan_user_link', 'message', 'created_at')
#     list_filter = ('clan_chat', 'clan_chat__clan__game')
#
#     @staticmethod
#     def message(objects):
#         text = objects.text
#         return text[:min(len(text), 20)] + '...'
#
#     @staticmethod
#     def clan_user_link(objects):
#         return _link_to(objects, 'game_gameclanmember_change', objects.user.id, objects.user)
