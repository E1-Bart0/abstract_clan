from django.contrib.auth.models import User
from django.db import models


class ClanUserRole(models.IntegerChoices):
    admin = 0, 'admin'
    player = 1, 'player'


class ClanUserABS(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    role = models.PositiveSmallIntegerField(choices=ClanUserRole.choices, default=1)
    entry = models.DateTimeField(auto_now_add=True)
    clan = None

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        if self.clan.users_count == 1:
            self.clan.delete()
        return super().delete(*args, **kwargs)


class ClanInfoABS(models.Model):
    description = models.TextField(default='Clan description')
    rating = models.IntegerField(default=0)

    class Meta:
        abstract = True


class ClanSettingsABS(models.Model):
    open_close = models.BooleanField(default=True)
    min_rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ClanChatABS(models.Model):
    type = models.CharField(max_length=30, default='message')
    text = models.TextField(null=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    clan = None
    user = None

    class Meta:
        abstract = True


class ClanABS(models.Model):
    name = models.CharField(max_length=60, unique=True)
    info = None
    settings = None
    objects = None

    clan_users = None
    chat = None

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

    @property
    def get_users(self):
        return self.clan_users.all()

    @property
    def users_count(self):
        return self.get_users.count()

    @property
    def get_messages(self):
        return self.chat.all()

    def update_info(self, **kwargs):
        info = self.info.__dict__
        for key, value in kwargs.items():
            if key not in info:
                raise ModuleNotFoundError(f'Not field "{key}" in Clan Info')
            info[key] = value
        self.info.save()

    def update_settings(self, **kwargs):
        settings = self.settings.__dict__
        for key, value in kwargs.items():
            if key not in settings:
                raise ModuleNotFoundError(f'Not field "{key}" in Clan Settings')
            settings[key] = value
        self.settings.save()

    @property
    def oldest_user(self):
        return self.clan_users.order_by('entry').first()

    def send_msg(self, user, **kwargs):
        clan_user = self.clan_users.filter(user=user).first()
        msg = self.chat.create(clan=self, clan_user=clan_user, type='message', **kwargs)
        return msg

    def send_request(self, user, **kwargs):
        clan_user = self.clan_users.filter(user=user).first()
        msg = self.chat.create(clan=self, clan_user=clan_user, type='request', **kwargs)
        return msg

    def get_all_user_msgs(self, user):
        clan_user = self.clan_users.filter(user=user).first()
        return clan_user.clan_user_msgs.all()

    def join(self, user, **kwargs):
        clan_user = self.clan_users.create(clan=self, user=user, **kwargs)
        return clan_user

    def exit(self, user):
        clan_user = self.clan_users.filter(user=user)
        if clan_user.exists():
            clan_user = clan_user.first()
            clan_user_role = clan_user.role
            clan_user.delete()

            if not self.users_count:
                return
            self.change_admin(clan_user_role)

    def change_admin(self, clan_user_role):
        if clan_user_role == ClanUserRole.admin and not \
                len(list(filter(lambda u: u.role == ClanUserRole.admin, self.get_users))):
            self.give_admin(self.oldest_user)

    def give_admin(self, user):
        clan_user = self.clan_users.filter(user=user)
        if clan_user.exists():
            clan_user = clan_user.first()
            clan_user.role = ClanUserRole.admin
            clan_user.save()

    def delete(self, *args, **kwargs):
        self.info.delete()
        self.settings.delete()
        return super().delete(*args, **kwargs)

