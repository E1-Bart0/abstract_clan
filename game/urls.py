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
from .views import clan_views

urlpatterns = [
    path('clans_all/', clan_views.ClanListView.as_view(), name='clans'),
    path(r'clan/', clan_views.ClanView.as_view(), name='clan'),

    path('clan/actions/create/', clan_views.CreateClanView.as_view(), name='clan-create'),
    path('clan/actions/update/', clan_views.UpdateClanView.as_view(), name='clan-update'),
    path('clan/actions/delete/', clan_views.DeleteClanView.as_view(), name='clan-update'),
]
