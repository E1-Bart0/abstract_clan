from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from game.serializers.clan_members_serializers import (
    ClanMembersListSerializer,
    ClanMemberSerializer,
    ClanMemberJoinSerializer
)


class ClanMembersListView(APIView):
    serializer_class = ClanMembersListSerializer
    model = serializer_class.Meta.model

    def get(self, request):
        clan_id = self._get_clan_id_from(request, 'clan_id')
        clan = self.model.objects.filter(id=clan_id)
        if clan.exists():
            clan = clan.first()
            return Response(self.serializer_class(clan).data, status.HTTP_200_OK)
        return Response({'Error': f'No clan with such id "{clan_id}"'}, status.HTTP_404_NOT_FOUND)

    @staticmethod
    def _get_clan_id_from(request, param):
        clan_id = request.GET.get(param)
        if not clan_id:
            if hasattr(request.user, 'clan_member'):
                clan_id = request.user.clan_member.clan.id
        return clan_id


class ClanMemberView(APIView):
    serializer_class = ClanMemberSerializer
    model = serializer_class.Meta.model

    def get(self, request):
        member_id = self._get_member_id_from(request)
        clan_member = self.model.objects.filter(user_id=member_id)
        if clan_member.exists():
            return Response(self.serializer_class(clan_member.first()).data, status=status.HTTP_200_OK)
        return Response({'Error': f'Clan member with such id "{member_id}" does not exist'}, status.HTTP_404_NOT_FOUND)

    @staticmethod
    def _get_member_id_from(request):
        member_id = request.GET.get('id')
        if not member_id and hasattr(request.user, 'clan_member'):
            member_id = request.user.id
        return member_id


class ClanMemberJoinView(APIView):
    serializer_class = ClanMemberJoinSerializer
    model = serializer_class.Meta.model

    def post(self, request):
        data = self._get_data_from(request)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.add_member()
        return Response({'OK': f'User was joined the clan'})

    @staticmethod
    def _get_data_from(request):
        data = {
            'id': request.GET.get('id') or request.GET.get('clan_id'),
            'user': request.user.id
        }
        return data


class ClanMemberLeaveView(APIView):

    @staticmethod
    def post(request):
        user = request.user
        if hasattr(user, 'clan_member'):
            clan = user.clan_member.clan
            clan.remove(user)
            return Response({'OK': f'User was removed from the clan'}, status.HTTP_200_OK)
        return Response({'Error': 'User not in clan'}, status.HTTP_400_BAD_REQUEST)
