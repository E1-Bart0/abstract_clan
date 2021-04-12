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
        self.clan.refresh_from_db()
        self.assertEqual(self.clan.creator, self.user)
        self.assertEqual(self.clan.creator.clan_member.clan, self.clan)
        self.assertTrue(self.clan.chat)

        with self.assertRaises(django.db.utils.IntegrityError):
            clan = GameClan.create(creator=self.user, name='Test')

    def test_add__remove(self):
        new_user = self._add_n_users(1)[0]
        self.clan.add(new_user)
        self.assertEqual([self.user, new_user], [clan_member.user for clan_member in self.clan.members.all()])

        self.clan.remove(new_user)
        self.assertEqual([self.user], [clan_member.user for clan_member in self.clan.members.all()])
        self.clan.remove(self.user)
        self._test_clan_does_not_exist()

    def test_join__leave(self):
        new_user = self._add_n_users(1)[0]
        GameClanMember.join(user=new_user, clan=self.clan)
        self.assertEqual([self.user, new_user], [clan_member.user for clan_member in self.clan.members.all()])

        new_user.clan_member.leave()

        self.assertEqual([self.user], [clan_member.user for clan_member in self.clan.members.all()])
        self.user.clan_member.leave()
        self._test_clan_does_not_exist()

    def test_notification__in_add_remove_join_leave(self):
        new_user1, new_user2 = self._add_n_users(2)
        self.clan.add(new_user1)
        GameClanMember.join(user=new_user2, clan=self.clan)
        self.clan.remove(user=new_user2)
        new_user1.clan_member.leave()

        self.assertEqual(5, self.clan.chat.notifications.count())

    def _test_clan_does_not_exist(self):
        with self.assertRaises(GameClan.DoesNotExist):
            self.clan.refresh_from_db()

    @staticmethod
    def _add_n_users(n):
        return [User.objects.create_user(username=f'Test{user}', password='bla4321') for user in range(n)]

    def test_next_creator_when_leaving(self):
        new_user = self._add_n_users(1)[0]
        self.clan.add(new_user)
        self.clan.remove(self.user)
        self.clan.refresh_from_db()

        self.assertEqual(new_user, self.clan.creator)

    def test_send_text_messages(self):
        text = 'TestMessage'
        msg = self.clan.chat.send(user=self.user, request_type='message', text=text)
        msg.refresh_from_db()

        self.assertEqual(self.clan.chat.messages.first().text, text)
        self.assertEqual(self.user.my_messages.first().text, text)

    def test_max_150_messages(self):
        max_count = 150
        create_count = 200
        [self.clan.chat.send(user=self.user, text=f'TestMsg{i}', request_type='message') for i in range(create_count)]
        self.assertEqual(max_count, self.clan.chat.messages.count())
        self.assertEqual(self.clan.chat.messages.order_by('created_at').first().text, f'TestMsg{create_count-max_count}')

    def test_send_resource_request(self):
        msg = self.clan.chat.send(user=self.user, request_type='resource_requests')
        msg.refresh_from_db()
        self.assertEqual(1, self.clan.chat.resource_requests.count())

    def test_send_item_request(self):
        msg = self.clan.chat.send(user=self.user, request_type='item_requests')
        msg.refresh_from_db()
        self.assertEqual(1, self.clan.chat.item_requests.count())

    def test_get_all_messages(self):
        text = 'Test_Message'
        msg = self.clan.chat.send(user=self.user, request_type='message', text=text)
        msg = self.clan.chat.send(user=self.user, request_type='resource_requests')
        msg = self.clan.chat.send(user=self.user, request_type='item_requests')
        self.assertEqual(4, len(self.clan.chat.all_messages))