from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from game.models import GameClan
from game.serializer import ClanListSerializer


class ListCreateClanView(ListCreateAPIView):
    serializer_class = ClanListSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        return self.model.objects.all()

    def post(self, request, *args, **kwargs):
        checked_data = self.serializer_class(data=request.data, context={'request': request})
        if checked_data.is_valid():
            print(checked_data.data)
            checked_data.save()
            return Response({}, status.HTTP_201_CREATED)
        else:
            print('aa', checked_data.errors)
            return Response(checked_data.errors, status=status.HTTP_400_BAD_REQUEST)





