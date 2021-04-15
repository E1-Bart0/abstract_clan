from django.db import models

User = 'myuser.User'


class ClanMemberABC(models.Model):
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

    def delete(self, *args, **kwargs):
        """Deleting Clan Model
         Sending notification about leaving"""
        if hasattr(self.clan, 'chats'):
            text_on_join = f'{self.user.username} Leaving Your Clan'
            self.clan.chat.send(user=self.user, type='notification', text=text_on_join)
        if self.clan.members.count() == 1:
            self.clan.delete()
        return super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Saving Clan Model. Sending notification about leaving"""
        if hasattr(self.clan, 'chats'):
            text_on_join = f'{self.user.username} Joining Your Clan'
            self.clan.chat.send(user=self.user, type='notification', text=text_on_join)
        return super().save(*args, **kwargs)

    @classmethod
    def create(cls, **kwargs):
        return super().save()

    @classmethod
    def join(cls, user, clan):
        """Adding user to ClanUsers"""
        clan_member = cls.objects.create(user=user, clan=clan)
        return clan_member

    def leave(self):
        """Delete clan_user when he leaving And sending notification about it"""
        self.delete()

    def __str__(self):
        return f'Clan member: {self.user.username}'

    class Meta:
        abstract = True
