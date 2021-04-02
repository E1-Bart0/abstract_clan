from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .serializers import ClanSerializer


class JoinClan(ListAPIView):
    serializer_class = ClanSerializer
