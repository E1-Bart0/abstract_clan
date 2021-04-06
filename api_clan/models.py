from django.contrib.auth.models import User
from django.db import models


class ClanUserABS(models.Model):
    """
    Abstract model for Clan User.
    !!! When inherit: clan -> Ref to your Clan model needed with related_name 'clan_users'

        Example:
        clan = models.ForeignKey(GameClan, on_delete=models.CASCADE, related_name='clan_users')
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='clan_profile')
    clan = None
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        """Deleting Clan Model if no users and remove msgs"""
        self.user.my_msgs.all().delete()
        if self.clan.clan_users.count() == 1:
            self.clan.delete()
        return super().delete(*args, **kwargs)

    @classmethod
    def join(cls, user, clan):
        """Adding user to ClanUsers"""
        return cls.objects.create(user=user, clan=clan)

    def leave(self):
        """Delete clan_user when he leaving"""
        self.delete()


class ClanChatABS(models.Model):
    """
    Abstract model for Clan Chat.
    !!! When inherit: clan -> Ref to your Clan model needed with related_name 'chat'

        Example:
        clan = models.ForeignKey(GameClan, on_delete=models.CASCADE, related_name='chats')
    """
    clan = None

    class Meta:
        abstract = True

    def send(self, user, **kwargs):
        self.max_150_msgs()
        return self.msgs.create(user=user, **kwargs)

    def max_150_msgs(self, max_count=150):
        msgs_count = self.msgs.all().count()
        if msgs_count >= max_count:
            [msg.delete() for msg in self.msgs.order_by('created_at')[:msgs_count - max_count + 1]]


class ChatMessages(models.Model):
    """
    Abstract model for Chat Messages.
    !!! When inherit: clan_chat -> Ref to your Chat model needed with related_name 'msgs'

        Example:
        clan_chat = models.ForeignKey(GameClanChat, on_delete=models.CASCADE, related_name='msgs')
    """

    clan_chat = None
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_msgs')
    type = models.CharField(max_length=30, default='message')
    text = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ClanABS(models.Model):
    """
    Abstract model for Clan.
    !!! When inherit: game -> Ref to your Game model.
    """
    name = models.CharField(max_length=60, unique=True)
    description = models.TextField(default=' ')
    creator = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='my_clan')
    max_users = models.IntegerField(default=60)
    created_at = models.DateTimeField(auto_now_add=True)
    game = None

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

    @classmethod
    def create(cls, **kwargs):
        """
        Creating ClanUser(), ClanChat with Clan creation
        """
        clan = cls(**kwargs)
        clan.save()
        clan.add(user=kwargs['creator'])
        try:
            clan.chats.create(clan=clan)
        except AttributeError:
            pass
        return clan

    def next_creator(self):
        """Changing Clan creator to oldest user"""
        self.creator = self.clan_users.order_by('joined_at').first().user
        self.save(update_fields=['creator'])

    def add(self, user, **kwargs):
        """Create new ClanUser"""
        clan_user = self.clan_users.create(clan=self, user=user, **kwargs)
        return clan_user

    def remove(self, user):
        """Deleting ClanUser. If user is admin checking others users and if no more admins in clan,
            making oldest user admin"""
        user.clan_profile.delete()
        if self.creator == user and self.clan_users.count():
            self.next_creator()

    @property
    def chat(self):
        """:return ClanChat"""
        return self.chats.first()
