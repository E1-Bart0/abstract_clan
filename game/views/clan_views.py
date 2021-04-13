from rest_framework import status
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.views import APIView

from game.serializers.clan_serializer import *


class ClanListView(ListAPIView):
    serializer_class = ClanListSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()


class ClanView(ListAPIView):
    serializer_class = ClanDetailUpdateSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        clan_id = self.request.GET.get('id')
        if not clan_id:
            if hasattr(self.request.user, 'my_clan'):
                clan_id = self.request.user.my_clan.id
        return self.model.objects.filter(id=clan_id)


class CreateClanView(CreateAPIView):
    serializer_class = ClanCreateSerializer
    model = serializer_class.Meta.model

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({}, status.HTTP_201_CREATED)


class UpdateClanView(UpdateAPIView):
    serializer_class = ClanDetailUpdateSerializer
    model = serializer_class.Meta.model

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context=request)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({}, status=status.HTTP_200_OK)


class DeleteClanView(APIView):
    serializer_class = ClanDetailUpdateSerializer
    model = serializer_class.Meta.model

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context=request)
        serializer.is_valid(raise_exception=True)
        serializer.delete_model()
        return Response({}, status=status.HTTP_200_OK)

# class ClanAddMemberView(APIView):
#
#     def post(self, request):
#         if hasattr(self.request.user, '')

