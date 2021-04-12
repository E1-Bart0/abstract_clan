from django.db import models

User = 'myuser.User'


class ChatMessageABC(models.Model):
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

    def __str__(self):
        return f'Clan name: {self.clan_chat.clan.name}| Chat: {self.clan_chat.name}'

    class Meta:
        abstract = True
