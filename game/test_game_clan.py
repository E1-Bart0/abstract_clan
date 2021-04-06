import django
from django.contrib.auth.models import User
from django.test import TestCase

from game.models import GameClan, GameClanUser


class GameClanTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='Test', password='bla4321')
        self.clan = GameClan.create(creator=self.user, name='TestClan')

    def test_creation_clan(self):
        self.clan.refresh_from_db()
        self.assertEqual(self.clan.creator, self.user)
        self.assertEqual(self.clan.creator.clan_profile.clan, self.clan)

        with self.assertRaises(django.db.utils.IntegrityError):
            clan = GameClan.create(creator=self.user, name='Test')

    def test_add__remove(self):
        new_user = self._add_n_users(1)[0]
        self.clan.add(new_user)
        self.assertEqual([self.user, new_user], [clan_user.user for clan_user in self.clan.clan_users.all()])

        self.clan.remove(new_user)
        self.assertEqual([self.user], [clan_user.user for clan_user in self.clan.clan_users.all()])
        self.clan.remove(self.user)
        self._test_clan_does_not_exist()

    def test_join__leave(self):
        new_user = self._add_n_users(1)[0]
        GameClanUser.join(user=new_user, clan=self.clan)
        self.assertEqual([self.user, new_user], [clan_user.user for clan_user in self.clan.clan_users.all()])

        new_user.clan_profile.leave()

        self.assertEqual([self.user], [clan_user.user for clan_user in self.clan.clan_users.all()])
        self.user.clan_profile.leave()
        self._test_clan_does_not_exist()

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

    def test_send_messages(self):
        text = 'TestMessage'
        msg = self.clan.chat.send(user=self.user, text=text)
        msg.refresh_from_db()

        self.assertEqual(self.clan.chat.msgs.first().text, text)
        self.assertEqual(self.user.my_msgs.first().text, text)

    def test_max_150_messages(self):
        max_count = 150
        create_count = 200
        [self.clan.chat.send(user=self.user, text=f'TestMsg{i}') for i in range(create_count)]
        self.assertEqual(max_count, self.clan.chat.msgs.count())
        self.assertEqual(self.clan.chat.msgs.order_by('created_at').first().text, f'TestMsg{create_count-max_count}')
