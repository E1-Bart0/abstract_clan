from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from game.models import GameClan
from game.serializer import ClanListSerializer, ClanUsersListSerializer, ClanChatSerializer


class ClanUsersList(ListAPIView):
    serializer_class = ClanUsersListSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        clan_name = self.request.query_params.get('clan')
        if clan_name:
            queryset = self.model.objects.filter(clan__name=clan_name)
        else:
            queryset = self.model.objects.all()
        return queryset


class ClanList(ListAPIView):
    serializer_class = ClanListSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        return self.model.objects.all()


class ClanChatList(ListAPIView):
    serializer_class = ClanChatSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        clan_name = self.request.query_params.get('clan')
        if clan_name:
            queryset = self.model.objects.filter(clan__name=clan_name)
        else:
            queryset = self.model.objects.all()
        return queryset
