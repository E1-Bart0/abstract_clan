from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from game.tests.test_clan_member_views import TestPrepareClientClanUser
from myuser.models import User


class TestChatViews(TestPrepareClientClanUser):

    def test_chat_view(self):
        """TEST VIEW ClanChatView OK (GET): Get GameClanChat with all Messages"""
        url = reverse('clan-chat')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        clan_id_param = '?clan_id=1'
        response = self.client.get(url + clan_id_param)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_chat_view__invalid_user(self):
        """TEST VIEW ClanChatView BAD REQUEST (GET): Get GameClanChat with all Messages,
            But User not in clan"""
        self.user.clan_member.leave()

        url = reverse('clan-chat')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_chat_view__invalid_param(self):
        """TEST VIEW ClanChatView BAD REQUEST (GET): Get GameClanChat with all Messages,
            But clan_id with such param does not exist"""

        url = reverse('clan-chat')
        clan_id_param = '?clan_id=2'
        response = self.client.get(url + clan_id_param)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_send_text(self):
        """TEST VIEW ClanChatSendAllView OK (POST): Send msg to GameChat"""
        url = reverse('clan-chat-send-text')
        data = {'text': 'Test Message'}

        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_send_text__invalid_user(self):
        """TEST VIEW ClanChatSendAllView BAD REQUEST (POST): Send msg to GameChat,
            But User not in clan"""
        self.user.clan_member.leave()
        url = reverse('clan-chat-send-text')
        data = {'text': 'Test Message'}

        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_request_resource(self):
        """TEST VIEW ClanChatSendAllView OK (POST): Send request_resource to GameChat"""
        url = reverse('clan-chat-request-resource')

        response = self.client.post(url)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_request_item(self):
        """TEST VIEW ClanChatSendAllView OK (POST): Send request_item to GameChat"""
        url = reverse('clan-chat-request-item')

        response = self.client.post(url)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_share_request_resource(self):
        """TEST VIEW ClanChatShareAllRequest OK (POST): Interact with existing request"""
        new_user = User.objects.create(username='Test1', password='Blabla4321')
        self.clan.add(new_user)
        new_user.clan_member.clan.chat.send(user=new_user, type='request_resource')
        url = reverse('clan-chat-request-resource-share')
        param = '?id=1'

        response = self.client.post(url + param)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_share_request_resource__invalid_param(self):
        """TEST VIEW ClanChatShareAllRequest BAD REQUEST (POST): Interact with existing request,
            But request with such id does not exist"""
        url = reverse('clan-chat-request-resource-share')
        param = '?id=10'

        response = self.client.post(url + param)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_share_request_resource__invalid_user_share_his_own_request(self):
        """TEST VIEW ClanChatShareAllRequest BAD REQUEST (POST): Interact with existing request,
            But it is his own request"""
        url = reverse('clan-chat-request-resource-share')
        param = '?id=1'

        response = self.client.post(url + param)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_share_request_resource__invalid_user(self):
        """TEST VIEW ClanChatShareAllRequest BAD REQUEST (POST): Interact with existing request,
            But user not in clan"""
        new_user = User.objects.create(username='Test1', password='Blabla4321')
        new_client = APIClient()
        new_client.force_authenticate(user=new_user)
        self.user.clan_member.clan.chat.send(user=self.user, type='request_resource')

        url = reverse('clan-chat-request-resource-share')
        param = '?id=1'

        response = self.client.post(url + param)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_share_request_item(self):
        """TEST VIEW ClanChatShareAllRequest OK (POST): Interact with existing request"""
        new_user = User.objects.create(username='Test1', password='Blabla4321')
        self.clan.add(new_user)
        new_user.clan_member.clan.chat.send(user=new_user, type='request_item')
        url = reverse('clan-chat-request-item-share')
        param = '?id=1'

        response = self.client.post(url + param)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
