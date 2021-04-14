from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from game.serializers.clan_members_serializer import ClanMembersListSerializer


class ClanMembersListView(APIView):
    serializer_class = ClanMembersListSerializer
    model = serializer_class.Meta.model

    def get(self, request):
        clan_id = request.GET.get('id')
        clan = self.model.objects.filter(id=clan_id)
        if clan.exists():
            clan = clan.first()
            return Response(self.serializer_class(clan).data, status.HTTP_200_OK)
        return Response({'Error': f'No clan with such id "{clan_id}"'}, status.HTTP_404_NOT_FOUND)



