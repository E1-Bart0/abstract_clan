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
        """Testing clan list view"""
        n = 5
        users = [User.objects.create(username=f'Test{index}', password='Blabla4321', game=self.game)
                 for index in range(n)]
        clans = [GameClan.create(creator=user, name=f'{user.username} Clan', description='TEST', game=self.game)
                 for user in users]

        url = reverse('clans')
        response = self.client.get(url)
        self.assertEqual(n, len(response.data))

    def test_creating_clan__creating_clan_member__creating_clan_chat(self):
        """Testing creating clan member and clan chat while creating clan"""
        url = reverse('clan-create')
        data = {"name": "Test", "description": "TestClan"}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user.my_clan.name, 'Test')
        self.assertEqual(self.user.my_clan.chat.name, 'Test')
        self.assertEqual(self.user.my_clan.creator, self.user)
        self.assertTrue(self.user.clan_member)

    def test_creating_clan__invalid_name(self):
        """Clan name should be unique"""
        clan_name = 'CLAN'
        new_user = User.objects.create(username=f'Test1', password='Blabla4321', game=self.game)
        clan = GameClan.create(creator=new_user, name=f'{clan_name}', description='TEST', game=self.game)

        url = reverse('clan-create')
        data = {"name": clan_name, "description": "TestClan"}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_clan__invalid_creator(self):
        """Creator must be unique and have a game"""
        clan = GameClan.create(creator=self.user, name='TEST', description='TEST', game=self.game)

        url = reverse('clan-create')
        data = {"name": 'Test1', "description": "TestClan"}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        new_client = APIClient()
        new_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_clan_detail_view(self):
        """Test Ok clan view"""
        new_user = User.objects.create(username=f'Test1', password='Blabla4321', game=self.game)
        clan = GameClan.create(creator=new_user, name='TEST1', description='TEST', game=self.game)
        clan = GameClan.create(creator=self.user, name='TEST', description='TEST', game=self.game)
        url = reverse('clan')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url + '?id=2', )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_clan_detail_view__clan_not_exist(self):
        """If clan do not exists"""
        url = reverse('clan')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(url + '?id=2')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_clan_update(self):
        """Updating clan"""
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
        """Trying update clan that does not exists"""
        url = reverse('clan-update')
        data = {'name': 'Test1', 'description': 'TEST!', 'max_members': 2}
        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_clan_update__invalid_user(self):
        """Trying update, but not from creator"""
        new_user = User.objects.create(username=f'Test1', password='Blabla4321', game=self.game)
        clan = GameClan.create(creator=new_user, name='TEST1', description='TEST', game=self.game)

        url = reverse('clan-update')
        data = {'name': 'Test1', 'description': 'TEST!', 'max_members': 2}
        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_clan_update__invalid_unique_name(self):
        """If such clan name already exists"""
        new_user = User.objects.create(username=f'Test1', password='Blabla4321', game=self.game)
        clan2 = GameClan.create(creator=new_user, name='TEST1', description='TEST', game=self.game)
        clan1 = GameClan.create(creator=self.user, name='TEST2', description='TEST', game=self.game)

        url = reverse('clan-update')
        data = {'name': 'TEST1', 'description': 'TEST!', 'max_members': 2}
        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_clan_delete(self):
        """Deleting clan"""
        new_user = User.objects.create(username=f'Test1', password='Blabla4321', game=self.game)
        clan = GameClan.create(creator=self.user, name='TEST', description='TEST', game=self.game)

        url = reverse('clan-delete')
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_clan_add_member(self):
        new_user = User.objects.create(username=f'Test1', password='Blabla4321', game=self.game)
        clan = GameClan.create(creator=new_user, name='TEST', description='TEST', game=self.game)

        url = reverse('clan-add-member') + f'?id={clan.id}'
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_clan_add_member_invalid__already_in_clan(self):
        clan = GameClan.create(creator=self.user, name='TEST', description='TEST', game=self.game)

        url = reverse('clan-add-member') + f'?id={clan.id}'
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_clan_remove_member(self):
        clan = GameClan.create(creator=self.user, name='TEST', description='TEST', game=self.game)

        url = reverse('clan-remove-member')
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_clan_remove_invalid__user_not_in_clan(self):

        url = reverse('clan-remove-member')
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
