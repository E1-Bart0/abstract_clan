from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from game.serializers.clan_members_serializers import ClanMembersListSerializer, ClanMemberSerializer
from game.views.clan_views import AddClanMemberView, RemoveClanMemberView


class ClanMembersListView(APIView):
    serializer_class = ClanMembersListSerializer
    model = serializer_class.Meta.model

    def get(self, request):
        clan_id = request.GET.get('clan_id')
        if not clan_id:
            if hasattr(request.user, 'clan_member'):
                clan_id = request.user.clan_member.clan.id
        clan = self.model.objects.filter(id=clan_id)
        if clan.exists():
            clan = clan.first()
            return Response(self.serializer_class(clan).data, status.HTTP_200_OK)
        return Response({'Error': f'No clan with such id "{clan_id}"'}, status.HTTP_404_NOT_FOUND)


class ClanMemberView(APIView):
    serializer_class = ClanMemberSerializer
    model = serializer_class.Meta.model

    def get(self, request):
        member_id = self.request.GET.get('id')
        if not member_id and hasattr(self.request.user, 'clan_member'):
            member_id = self.request.user.id
        clan_member = self.model.objects.filter(user_id=member_id)
        if clan_member.exists():
            return Response(self.serializer_class(clan_member.first()).data, status=status.HTTP_200_OK)
        return Response({'Error': f'Clan member with such id "{member_id}" does not exist'}, status.HTTP_404_NOT_FOUND)


class ClanMemberJoinView(AddClanMemberView):
    pass


class ClanMemberLeaveView(RemoveClanMemberView):
    pass
