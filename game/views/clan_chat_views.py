from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from game.serializers.clan_chat_serializers import ChatSerializer, SendSerializer, ShareSerializer
from game.views.clan_member_views import ClanMembersListView


class ClanChatView(ClanMembersListView):
    serializer_class = ChatSerializer
    model = serializer_class.Meta.model

    def get(self, request):
        clan_id = request.GET.get('clan_id')
        user = request.user
        if not clan_id:
            if hasattr(user, 'clan_member') and hasattr(user.clan_member.clan, 'chat'):
                clan_id = request.user.clan_member.clan.id
        chat = self.model.objects.filter(clan_id=clan_id)
        if chat.exists():
            chat = chat.first()
            return Response(self.serializer_class(chat).data, status.HTTP_200_OK)
        return Response({'Error': f'No clan with such id "{clan_id}"'}, status.HTTP_404_NOT_FOUND)


class ClanChatSendAllViews(APIView):
    serializer_class = SendSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data, context=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({}, status.HTTP_201_CREATED)


class ClanChatShareAllRequest(ClanChatSendAllViews):
    serializer_class = ShareSerializer
