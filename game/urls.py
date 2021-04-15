"""cfg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import clan_views, clan_member_views, clan_chat_views

urlpatterns = [
    path('clan', clan_views.ClanView.as_view(), name='clan'),
    path('clan/list', clan_views.ClanListView.as_view(), name='clans'),

    path('clan/create', clan_views.CreateClanView.as_view(), name='clan-create'),
    path('clan/update', clan_views.UpdateClanView.as_view(), name='clan-update'),
    path('clan/delete', clan_views.DeleteClanView.as_view(), name='clan-delete'),
    path('clan/remove_member', clan_views.RemoveClanMemberView.as_view(), name='clan-remove-member'),

    path('clan/member/list', clan_member_views.ClanMembersListView.as_view(), name='clan-members'),
    path('clan/member', clan_member_views.ClanMemberView.as_view(), name='clan-member'),
    path('clan/member/join', clan_member_views.ClanMemberJoinView.as_view(), name='clan-member-join'),
    path('clan/member/leave', clan_member_views.ClanMemberLeaveView.as_view(), name='clan-member-leave'),

    path('clan/chat', clan_chat_views.ClanChatView.as_view(), name='clan-chat'),
    path('clan/chat/send_text', clan_chat_views.ClanChatSendAllViews.as_view(), name='clan-chat-send-text'),
    path('clan/chat/request_resource', clan_chat_views.ClanChatSendAllViews.as_view(),
         name='clan-chat-request-resource'),
    path('clan/chat/request_item', clan_chat_views.ClanChatSendAllViews.as_view(), name='clan-chat-request-item'),

    path('clan/chat/request_resource/share', clan_chat_views.ClanChatShareAllRequest.as_view(),
         name='clan-chat-request-resource-share'),
    path('clan/chat/request_item/share', clan_chat_views.ClanChatShareAllRequest.as_view(),
         name='clan-chat-request-item-share'),
]
