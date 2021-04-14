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
from .views import clan_views, clan_members_view

urlpatterns = [
    path('clans', clan_views.ClanListView.as_view(), name='clans'),
    path('clan', clan_views.ClanView.as_view(), name='clan'),

    path('clan/create', clan_views.CreateClanView.as_view(), name='clan-create'),
    path('clan/update', clan_views.UpdateClanView.as_view(), name='clan-update'),
    path('clan/delete', clan_views.DeleteClanView.as_view(), name='clan-delete'),
    path('clan/add_member', clan_views.AddClanMemberView.as_view(), name='clan-add-member'),
    path('clan/remove_member', clan_views.RemoveClanMemberView.as_view(), name='clan-remove-member'),

    path('clan/members', clan_members_view.ClanMembersListView.as_view(), name='clan-members'),
    path('clan/member', clan_members_view.ClanMemberView.as_view(), name='clan-member'),
    path('clan/member/join', clan_members_view.ClanMemberJoinView.as_view(), name='clan-member-join'),
    path('clan/member/leave', clan_members_view.ClanMemberLeaveView.as_view(), name='clan-member-leave'),


]
