from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from game.serializers.clan_serializer import (
    ClanListSerializer,
    ClanDetailView,
    ClanCreateSerializer,
    ClanUpdateSerializer,
    ClanDeleteSerializer,
    AddClanMemberSerializer,
)


class ClanListView(ListAPIView):
    serializer_class = ClanListSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()


class ClanView(APIView):
    serializer_class = ClanDetailView
    model = serializer_class.Meta.model

    def get(self, request):
        clan_id = self.get_clan_id(request)
        clan = self.model.objects.filter(id=clan_id)
        if clan.exists():
            return Response(self.serializer_class(clan.first()).data, status=status.HTTP_200_OK)
        return Response({'Error': f'Clan with such id "{clan_id}" does not exist '}, status.HTTP_404_NOT_FOUND)

    @staticmethod
    def get_clan_id(request):
        clan_id = request.GET.get('id')
        if not clan_id and hasattr(request.user, 'my_clan'):
            clan_id = request.user.my_clan.id
        return clan_id


class CreateClanView(CreateAPIView):
    serializer_class = ClanCreateSerializer
    model = serializer_class.Meta.model

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"OK": "Clan was created"}, status.HTTP_201_CREATED)


class UpdateClanView(APIView):
    serializer_class = ClanUpdateSerializer
    model = serializer_class.Meta.model

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"OK": "Clan was updated"}, status=status.HTTP_200_OK)


class DeleteClanView(APIView):
    serializer_class = ClanDeleteSerializer
    model = serializer_class.Meta.model

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context=request)
        serializer.is_valid(raise_exception=True)
        serializer.delete_model()
        return Response({'OK': 'Clan was deleted'}, status=status.HTTP_200_OK)


class AddClanMemberView(APIView):
    serializer_class = AddClanMemberSerializer
    model = serializer_class.Meta.model

    def post(self, request):
        data = self.get_data_from(request)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.add_member()
        return Response({'OK': f'User was joined the clan'})

    @staticmethod
    def get_data_from(request):
        data = {
            'id': request.GET.get('id') or request.GET.get('clan_id'),
            'user': request.user.id
        }
        return data


class RemoveClanMemberView(APIView):

    @staticmethod
    def post(request):
        user = request.user
        if hasattr(user, 'clan_member'):
            clan = user.clan_member.clan
            clan.remove(user)
            return Response({'OK': f'User was removed from the clan'}, status.HTTP_200_OK)
        return Response({'Error': 'User not in clan'}, status.HTTP_400_BAD_REQUEST)
