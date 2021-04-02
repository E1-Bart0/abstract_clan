from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from game.models import GameClan
from game.serializer import ClanListSerializer


class GetAll(APIView):
    def get(self, request):
        clan = GameClan.objects.first()

        info = clan.info
        chat_messages = [{'msg': m.text, 'user': m.host.host.username} for m in clan.chat.all()]
        participants = [u.host.username for u in clan.clan_user.all()]

        response = {
            'clan_name': clan.name,
            'info': info.description,
            'participants': participants,
            'msgs': chat_messages,
        }

        print(response)
        return Response(response, status=status.HTTP_200_OK)
