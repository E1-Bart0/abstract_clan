from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from game.models import GameClan, GameClanMember, Game
from myuser.models import User


class ClanViewsTestCase(TestCase):

    def setUp(self):
        self.game = Game.objects.create(game='Test', slug='test')
        self.user = User.objects.create(username='TestUesr', password='Blabla4321', game=self.game)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_creating_clan(self):
        url = reverse('clans')
        data = {"name": "Test", "description": "TestClan"}

        response = self.client.post(url, data, format='json')
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user.my_clan.name, 'Test')
        self.assertEqual(self.user.my_clan.chat.name, 'Test')

