import django
from django.test import TestCase

from game.models import GameClan, GameClanMember, Game
from myuser.models import User


class GameClanTestCase(TestCase):

    def setUp(self) -> None:
        self.game = Game.objects.create()
        self.user = User.objects.create_user(username='Test', password='bla4321')
        self.clan = GameClan.create(creator=self.user, name='TestClan', game=self.game)

    def test_creation_clan__and_chat(self):
        """TEST MODEL GameClan OK: Creating GameChat, GameClanMember while creating GameClan"""
        self.clan.refresh_from_db()
        self.assertEqual(self.clan.creator, self.user)
        self.assertEqual(self.clan.creator.clan_member.clan, self.clan)
        self.assertTrue(self.clan.chat)

        with self.assertRaises(django.db.utils.IntegrityError):
            clan = GameClan.create(creator=self.user, name='Test')

    def test_add__remove(self):
        """TEST MODEL GameClan OK: Adding and Removing user to clan"""
        new_user = self._create_n_users(1)[0]
        self.clan.add(new_user)
        self.assertEqual([self.user, new_user], [clan_member.user for clan_member in self.clan.members.all()])

        self.clan.remove(new_user)
        self.assertEqual([self.user], [clan_member.user for clan_member in self.clan.members.all()])
        self.clan.remove(self.user)
        self._test_clan_does_not_exist()

    def test_join__leave(self):
        """TEST MODEL GameClanMember OK: Joining and Leaving user to clan"""
        new_user = self._create_n_users(1)[0]
        GameClanMember.join(user=new_user, clan=self.clan)
        self.assertEqual([self.user, new_user], [clan_member.user for clan_member in self.clan.members.all()])

        new_user.clan_member.leave()

        self.assertEqual([self.user], [clan_member.user for clan_member in self.clan.members.all()])
        self.user.clan_member.leave()
        self._test_clan_does_not_exist()

    def test_notification__in_add_remove_join_leave(self):
        """TEST MODEL GameClanChat OK: Sending notification about leaving and joining clan_member"""
        new_user1, new_user2 = self._create_n_users(2)
        self.clan.add(new_user1)
        GameClanMember.join(user=new_user2, clan=self.clan)
        self.clan.remove(user=new_user2)
        new_user1.clan_member.leave()

        self.assertEqual(5, self.clan.chat.notifications.count())

    def _test_clan_does_not_exist(self):
        with self.assertRaises(GameClan.DoesNotExist):
            self.clan.refresh_from_db()

    @staticmethod
    def _create_n_users(n):
        return [User.objects.create_user(username=f'Test{user}', password='bla4321') for user in range(n)]

    def test_next_creator_when_leaving(self):
        """TEST MODEL GameClan OK: Switching Clan creator to oldest clan_member
            if creator leaving"""
        new_user = self._create_n_users(1)[0]
        self.clan.add(new_user)
        self.clan.remove(self.user)
        self.clan.refresh_from_db()

        self.assertEqual(new_user, self.clan.creator)

    def test_send_text_messages(self):
        """TEST MODEL GameChat OK: Sending Text Message"""
        text = 'TestMessage'
        msg = self.clan.chat.send(user=self.user, type='send_text', text=text)
        msg.refresh_from_db()

        self.assertEqual(self.clan.chat.messages.first().text, text)
        self.assertEqual(self.user.my_messages.first().text, text)

    def test_max_150_messages(self):
        """TEST MODEL GameChat OK: Crop messages if Messages count > 150"""
        max_count = 150
        create_count = 200
        [self.clan.chat.send(user=self.user, text=f'TestMsg{i}', type='send_text') for i in range(create_count)]
        self.assertEqual(max_count, self.clan.chat.messages.count())
        self.assertEqual(self.clan.chat.messages.order_by('created_at').first().text, f'TestMsg{create_count-max_count}')

    def test_send_resource_request(self):
        """TEST MODEL GameChat OK: Sending Resource Request"""
        msg = self.clan.chat.send(user=self.user, type='request_resource')
        msg.refresh_from_db()
        self.assertEqual(1, self.clan.chat.requests_resource.count())

    def test_send_item_request(self):
        """TEST MODEL GameChat OK: Sending Item Request"""
        msg = self.clan.chat.send(user=self.user, type='request_item')
        msg.refresh_from_db()
        self.assertEqual(1, self.clan.chat.requests_item.count())

    def test_get_all_messages(self):
        """TEST MODEL GameChat OK: Get chat.all_messages queryset"""
        text = 'Test_Message'
        msg = self.clan.chat.send(user=self.user, type='send_text', text=text)
        msg = self.clan.chat.send(user=self.user, type='request_resource')
        msg = self.clan.chat.send(user=self.user, type='request_item')
        self.assertEqual(4, len(self.clan.chat.all_messages))