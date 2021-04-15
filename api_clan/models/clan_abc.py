from django.db import models

User = 'myuser.User'


class ClanABC(models.Model):
    """
    Abstract model for Clan.
    !!! When inherit: game -> Ref to your Game model.

        Example:
        game = models.ForeignKey(Game, on_delete=models.CASCADE)
    """
    name = models.CharField(max_length=60, null=False)
    description = models.TextField(default=' ')
    creator = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='my_clan')
    max_members = models.IntegerField(default=60)
    created_at = models.DateTimeField(auto_now_add=True)
    game = None

    @property
    def chats(self):
        return self.chats

    @property
    def members(self):
        return self.members

    @property
    def chat(self):
        return self.chats.first()

    @classmethod
    def create(cls, *args, **kwargs):
        """
        Creating ClanMember, ClanChat with Clan creation
        """
        clan = cls(*args, **kwargs)
        clan.save()
        if hasattr(clan, 'chats'):
            clan.chats.create(clan=clan, name=clan.name)
        clan.add(user=kwargs['creator'])
        return clan

    def change_creator(self):
        """Changing Clan creator to the oldest clan member. Sending notifications about it"""
        clan_member = self.members.order_by('joined_at').first()
        if hasattr(self, 'chats'):
            text_on_switch_creator = f'Creator: "{self.creator}" left, switching creator to "{clan_member.user}"'
            self.chat.send(user=clan_member.user, type='notification', text=text_on_switch_creator)
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

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('game', 'name',)
        abstract = True