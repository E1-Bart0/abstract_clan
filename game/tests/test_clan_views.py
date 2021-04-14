from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from game.models import GameClan, Game
from myuser.models import User


class ClanViewsTestCase(TestCase):

    def setUp(self):
        self.game = Game.objects.create(game='Test', slug='test')
        self.user = User.objects.create(username='TestUesr', password='Blabla4321', game=self.game)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_clan_list(self):
        """TEST VIEW ClanListView OK (GET): Get list of all clans"""
        n = 5
        users = [User.objects.create(username=f'Test{index}', password='Blabla4321', game=self.game)
                 for index in range(n)]
        clans = [GameClan.create(creator=user, name=f'{user.username} Clan', description='TEST', game=self.game)
                 for user in users]

        url = reverse('clans')
        response = self.client.get(url)
        self.assertEqual(n, len(response.data))

    def test_creating_clan__creating_clan_member__creating_clan_chat(self):
        """TEST VIEW ClanListView OK (GET): Creating ClanMember and ClanChat while creating clan"""
        url = reverse('clan-create')
        data = {"name": "Test", "description": "TestClan"}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user.my_clan.name, 'Test')
        self.assertEqual(self.user.my_clan.chat.name, 'Test')
        self.assertEqual(self.user.my_clan.creator, self.user)
        self.assertTrue(self.user.clan_member)

    def test_creating_clan__invalid_name(self):
        """TEST VIEW ClanListView BAD REQUEST (GET): Create clan if name not UNIQUE"""
        clan_name = 'CLAN'
        new_user = User.objects.create(username=f'Test1', password='Blabla4321', game=self.game)
        clan = GameClan.create(creator=new_user, name=f'{clan_name}', description='TEST', game=self.game)

        url = reverse('clan-create')
        data = {"name": clan_name, "description": "TestClan"}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_clan__invalid_creator(self):
        """TEST VIEW ClanListView BAD REQUEST (GET): Create clan, But creator must be UNIQUE and have a game"""
        clan = GameClan.create(creator=self.user, name='TEST', description='TEST', game=self.game)

        url = reverse('clan-create')
        data = {"name": 'Test1', "description": "TestClan"}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        new_client = APIClient()
        new_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_clan_detail_view(self):
        """TEST VIEW ClanView OK (GET): Get GameClan"""
        new_user = User.objects.create(username=f'Test1', password='Blabla4321', game=self.game)
        clan = GameClan.create(creator=new_user, name='TEST1', description='TEST', game=self.game)
        clan = GameClan.create(creator=self.user, name='TEST', description='TEST', game=self.game)
        url = reverse('clan')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url + '?id=2', )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_clan_detail_view__clan_not_exist(self):
        """TEST VIEW ClanView BAD REQUEST (GET): Get GameClan, But Clan not exist"""
        url = reverse('clan')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(url + '?id=2')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_clan_update(self):
        """TEST VIEW UpdateClanView OK (POST): Update GameClan"""
        clan = GameClan.create(creator=self.user, name='TEST1', description='TEST', game=self.game)

        url = reverse('clan-update')
        data = {'name': 'Test1', 'description': 'TEST!', 'max_members': 2}
        response = self.client.post(url, data)
        clan.refresh_from_db()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data['name'], clan.name)
        self.assertEqual(data['description'], clan.description)
        self.assertEqual(data['max_members'], clan.max_members)

    def test_clan_update__invalid_clan_id(self):
        """TEST VIEW UpdateClanView BAD REQUEST (POST): Update GameClan, But Clan do not exist"""
        url = reverse('clan-update')
        data = {'name': 'Test1', 'description': 'TEST!', 'max_members': 2}
        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_clan_update__invalid_user(self):
        """TEST VIEW UpdateClanView BAD REQUEST (POST): Update GameClan, But not from creator"""
        new_user = User.objects.create(username=f'Test1', password='Blabla4321', game=self.game)
        clan = GameClan.create(creator=new_user, name='TEST1', description='TEST', game=self.game)

        url = reverse('clan-update')
        data = {'name': 'Test1', 'description': 'TEST!', 'max_members': 2}
        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_clan_update__invalid_unique_name(self):
        """TEST VIEW UpdateClanView BAD REQUEST (POST): Update GameClan, But clan with such name already exist"""
        new_user = User.objects.create(username=f'Test1', password='Blabla4321', game=self.game)
        clan2 = GameClan.create(creator=new_user, name='TEST1', description='TEST', game=self.game)
        clan1 = GameClan.create(creator=self.user, name='TEST2', description='TEST', game=self.game)

        url = reverse('clan-update')
        data = {'name': 'TEST1', 'description': 'TEST!', 'max_members': 2}
        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_clan_delete(self):
        """TEST VIEW DeleteClanView OK (POST): Delete GameClan"""
        new_user = User.objects.create(username=f'Test1', password='Blabla4321', game=self.game)
        clan = GameClan.create(creator=self.user, name='TEST', description='TEST', game=self.game)

        url = reverse('clan-delete')
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_clan_add_member(self):
        """TEST VIEW AddClanMemberView OK (POST): Adding User to the GameClan"""
        new_user = User.objects.create(username=f'Test1', password='Blabla4321', game=self.game)
        clan = GameClan.create(creator=new_user, name='TEST', description='TEST', game=self.game)

        url = reverse('clan-add-member') + f'?id={clan.id}'
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_clan_add_member_invalid__already_in_clan(self):
        """TEST VIEW AddClanMemberView BAD REQUEST (POST): Adding User to the GameClan,
            But User already in the GameClan"""
        clan = GameClan.create(creator=self.user, name='TEST', description='TEST', game=self.game)

        url = reverse('clan-add-member') + f'?id={clan.id}'
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_clan_remove_member(self):
        """TEST VIEW RemoveClanMember OK (POST): Remove User from the GameClan"""
        clan = GameClan.create(creator=self.user, name='TEST', description='TEST', game=self.game)

        url = reverse('clan-remove-member')
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_clan_remove_invalid__user_not_in_clan(self):
        """TEST VIEW RemoveClanMemberView BAD REQUEST (POST): Removing User from the GameClan,
            But User not in the GameClan"""
        url = reverse('clan-remove-member')
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
