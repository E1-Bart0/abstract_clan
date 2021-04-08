from django.db import models
User = 'myuser.User'


class ClanMemberABS(models.Model):
    """
    Abstract model for Clan User.
    !!! When inherit: clan -> Ref to your Clan model needed with related_name 'members'

        Example:
        clan = models.ForeignKey(GameClan, on_delete=models.CASCADE, related_name='members')
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, related_name='clan_member')
    clan = None
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        """Deleting Clan Model if no users and remove messages"""
        self.user.my_messages.all().delete()
        if self.clan.members.count() == 1:
            self.clan.delete()
        return super().delete(*args, **kwargs)

    @classmethod
    def join(cls, user, clan):
        """Adding user to ClanUsers"""
        return cls.objects.create(user=user, clan=clan)

    def leave(self):
        """Delete clan_user when he leaving"""
        self.delete()

    def __str__(self):
        return f'Clan member: {self.user.username}'


class ClanChatABS(models.Model):
    """
    Abstract model for Clan Chat.
    !!! When inherit: clan -> Ref to your Clan model needed with related_name 'chat'

        Example:
        clan = models.ForeignKey(GameClan, on_delete=models.CASCADE, related_name='chats')
    """
    chat_id = models.AutoField(primary_key=True)
    clan = None
    name = models.CharField(max_length=30, null=True, unique=True)

    class Meta:
        abstract = True

    def send(self, user, **kwargs):
        self._crop_messages()
        return self.messages.create(user=user, **kwargs)

    def _crop_messages(self, max_messages=150):
        messages_count = self.messages.all().count()
        if messages_count >= max_messages:
            [msg.delete() for msg in self.messages.order_by('created_at')[:messages_count - max_messages + 1]]

    def __str__(self):
        return f'Clan {self.clan.name} | Chat: {self.name}'


class ChatMessageABS(models.Model):
    """
    Abstract model for Chat Messages.
    !!! When inherit: clan_chat -> Ref to your Chat model needed with related_name 'messages'

        Example:
        clan_chat = models.ForeignKey(GameClanChat, on_delete=models.CASCADE, related_name='messages')
    """
    id = models.AutoField(primary_key=True)
    clan_chat = None
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_messages')
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=30)
    text = None

    class Meta:
        abstract = True

    def __str__(self):
        return f'Clan name: {self.clan_chat.clan.name}| Chat: {self.clan_chat.name}'


class ClanABS(models.Model):
    """
    Abstract model for Clan.
    !!! When inherit: game -> Ref to your Game model.

        Example:
        game = models.ForeignKey(Game, on_delete=models.CASCADE)
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

    @property
    def chat(self):
        return self.chats.first()

    @classmethod
    def create(cls, **kwargs):
        """
        Creating ClanUser(), ClanChat with Clan creation
        """
        clan = cls(**kwargs)
        clan.save()
        clan.add(user=kwargs['creator'])
        try:
            clan.chats.create(clan=clan, name=clan.name)
        except AttributeError:
            pass
        return clan

    def change_creator(self):
        """Changing Clan creator to oldest user"""
        clan_member = self.members.order_by('joined_at').first()
        self.creator = clan_member.user
        self.save(update_fields=['creator'])

    def add(self, user, **kwargs):
        """Create new ClanUser"""
        clan_user = self.members.create(clan=self, user=user, **kwargs)
        return clan_user

    def remove(self, user):
        """Deleting ClanUser. If user is admin checking others users and if no more admins in clan,
            making oldest user admin"""
        user.clan_member.delete()
        if self.creator == user and self.members.count():
            self.change_creator()

