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
        self.clan = GameClan.create(name='TEST', description='Test', game=self.game, creator=self.user)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_clan_members_view(self):
        """TEST VIEW ClanMembersListView OK (GET): Get GameClan with more info about ClanMembers"""
        url = reverse('clan-members')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        clan_id_param = '?clan_id=1'
        response = self.client.get(url + clan_id_param)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_clan_members_view__invalid_clan_id(self):
        """TEST VIEW ClanMembersListView BAD REQUEST (GET): Get GameClan with more info about ClanMembers,
            But with Invalid param OR User without GameClan"""
        url = reverse('clan-members')
        clan_id_param = '?clan_id=2'
        self._get_bad_response_with_invalid_param(clan_id_param, url)
        self._get_bad_request_user_not_in_clan(url)

    def test_clan_member_view(self):
        """TEST VIEW ClanMemberView OK (GET): Get GameClanMember"""
        url = reverse('clan-member')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        param = '?id=1'
        response = self.client.get(url + param)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_clan_member_view__invalid_id(self):
        """TEST VIEW ClanMemberView BAD REQUEST (GET): Get GameClan,
            But with Invalid param OR User without GameClan"""
        url = reverse('clan-member')
        param = '?id=3'
        self._get_bad_response_with_invalid_param(param, url)
        self._get_bad_request_user_not_in_clan(url)

    def _get_bad_response_with_invalid_param(self, param, url):
        """Check BAD REQUEST on url with param"""
        response = self.client.get(url + param)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def _get_bad_request_user_not_in_clan(self, url):
        """Check BAD REQUEST on url but User not in clan"""
        self.clan.delete()
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_clan_member_join(self):
        """TEST VIEW ClanMemberJoinView OK (POST): Join User to the GameClan"""
        new_client, new_user = self._get_new_client__new_user()

        url = reverse('clan-member-join')
        param = '?clan_id=1'
        response = new_client.post(url + param, data={})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def _get_new_client__new_user(self):
        """Creating New Client From New User"""
        new_user = User.objects.create(username='Test1', password='blabla4321', game=self.game)
        new_client = APIClient()
        new_client.force_authenticate(new_user)
        return new_client, new_user

    def test_clan_member_join__invalid_user_already_in_clan(self):
        """TEST VIEW ClanMemberJoinView BAD REQUEST (POST): Join User to the GameClan,
            But User already in the GameClan"""
        url = reverse('clan-member-join')
        response = self.client.post(url, data={})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_clan_member_leave(self):
        """TEST VIEW ClanMemberRemoveView OK (POST): Remove User from the GameClan"""
        url = reverse('clan-member-leave')
        response = self.client.post(url, data={})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_clan_member_leave__invalid_user_not_in_clan(self):
        """TEST VIEW ClanMemberLeaveView BAD REQUEST (POST): Remove User from the GameClan,
            But User not in the GameClan"""
        new_client, new_user = self._get_new_client__new_user()
        url = reverse('clan-member-leave')
        response = new_client.post(url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
