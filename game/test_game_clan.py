from django.contrib.auth.models import User
from django.test import TestCase

from game.models import GameClan, GameClanUser, GameClanInfo, GameClanSettings, GameClanChat


class GameClanTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='Test', password='bla4321')

        self.clan = GameClan.objects.create(host=self.user, name='Test')
        self.info_desc_default = 'Clan description'
        self.info_rating_default = 0
        self.settings_open_close_default = True
        self.settings__min_rating_default = 0

    def test_create_game_clan(self):
        user = User.objects.create_user(username='TestCreate', password='bla4321')
        info = {'description': 'TestCreation description', }
        settings = {'open_close': False, }
        clan = GameClan.objects.create(host=user, name='TestCreate', info=info, settings=settings)

        self.assertEqual(user, clan.get_users.first().user)
        self.assertEqual([], list(clan.get_messages))
        self.assertEqual(info['description'], clan.info.description)
        self.assertEqual(self.info_rating_default, clan.info.rating)
        self.assertEqual(settings['open_close'], clan.settings.open_close)
        self.assertEqual(self.settings__min_rating_default, clan.settings.min_rating)
        self.assertEqual('TestCreate', clan.name)

    def test_update_info(self):
        description = 'test_update'
        rating = 54321
        self.clan.update_info(description=description, rating=rating)
        self.clan.refresh_from_db()

        self.assertEqual(self.clan.info.description, description)
        self.assertEqual(self.clan.info.rating, rating)

    def test_not_valid_update_info(self):
        description = 'test_update'
        rating = 54321
        not_needed = True
        with self.assertRaises(ModuleNotFoundError):
            self.clan.update_info(description=description, rating=rating, not_needed=not_needed)

        rating = 'NOT INT'
        with self.assertRaises(ValueError):
            self.clan.update_info(description=description, rating=rating)

    def test_update_settings(self):
        open_close = False
        min_rating = 10
        self.clan.update_settings(open_close=open_close, min_rating=min_rating)
        self.clan.refresh_from_db()

        self.assertEqual(self.clan.settings.open_close, open_close)
        self.assertEqual(self.clan.settings.min_rating, min_rating)

    def test_not_valid_update_settings(self):
        open_close = False
        min_rating = 10
        not_needed = True
        with self.assertRaises(ModuleNotFoundError):
            self.clan.update_settings(open_close=open_close, min_rating=min_rating, not_needed=not_needed)

        with self.assertRaises(ValueError):
            self.clan.update_settings(open_close=open_close, min_rating='aa')

    def test_join__users_count(self):
        n = 5
        self._create_n_users(n)

        self.assertEqual(n + 1, self.clan.users_count)

    def test_exit__give_admin__oldest_user(self):
        n = 5
        self._create_n_users(n)

        for i in range(n):
            oldest_user, next_oldest_user = GameClanUser.objects.order_by('entry')[0:2]
            self.clan.exit(user=oldest_user)
            next_oldest_user.refresh_from_db()
            self.assertEqual(n - i, self.clan.users_count)
            self.assertEqual(0, next_oldest_user.role)

    def _create_n_users(self, n, role=1):
        for i in range(n):
            user = User.objects.create_user(username=f'Test{i}', password='bla54321')
            self.clan.join(user=user, role=role)

    def test_msg_send(self):
        message = 'Test msg'
        self.clan.send_msg(user=self.user, text=message)
        msg = GameClanChat.objects.filter(clan=self.clan).first()
        self.assertEqual(msg.text, message)
        self.assertEqual(msg.type, 'message')

    def test_msg_request(self):
        message = 'Test msg'
        self.clan.send_request(user=self.user, text=message)
        msg = GameClanChat.objects.filter(clan=self.clan).first()
        self.assertEqual(msg.text, message)
        self.assertEqual(msg.type, 'request')

    def test_get_all_user_msgs(self):
        msgs = [self.clan.send_msg(user=self.user, text=f'Text{i} Msgs') for i in range(5)]
        saved_msg = self.clan.get_all_user_msgs(user=self.user)
        msgs_text = [f'Text{i} Msgs' for i in range(5)]
        self.assertEqual(msgs_text, [msg.text for msg in saved_msg])
        self.assertEqual(['Test'] * 5, [msg.clan_user.user.username for msg in saved_msg])

    def test_exit__deleting_clan(self):
        info = self.clan.info
        settings = self.clan.settings
        users = self.clan.clan_users.first()

        self.clan.exit(self.user)

        for model, main_model in zip((info, settings, users),
                                     (GameClanInfo, GameClanSettings, GameClanUser)):
            with self.assertRaises(main_model.DoesNotExist):
                model.refresh_from_db()

