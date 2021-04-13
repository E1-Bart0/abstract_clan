from itertools import chain

from django.db import models


class ClanChatABC(models.Model):
    """
    Abstract model for Clan Chat.
    !!! When inherit: clan -> Ref to your Clan model needed with related_name 'chats'

        Example:
        clan = models.ForeignKey(GameClan, on_delete=models.CASCADE, related_name='chats')
    """
    chat_id = models.AutoField(primary_key=True)
    clan = None
    name = models.CharField(max_length=30, null=True)

    @property
    def messages(self):
        return self.messages

    @property
    def resource_requests(self):
        return self.resource_requests

    @property
    def item_requests(self):
        return self.item_requests

    @property
    def notifications(self):
        return self.notifications

    @property
    def all_messages(self):
        text_messages = self.messages.all()
        resource_request = self.resource_requests.all()
        item_requests = self.item_requests.all()
        notifications = self.notifications.all()
        all_msgs = text_messages.union(resource_request, item_requests, notifications)
        return all_msgs

    def send(self, user, request_type, **kwargs):
        model = {
            'message': self.messages,
            'resource_requests': self.resource_requests,
            'item_requests': self.item_requests,
            'notification': self.notifications,
        }
        self._crop(model[request_type])
        response = model[request_type].create(user=user, **kwargs)
        return response

    @staticmethod
    def _crop(model, max_count=150):
        """Delete messages if they amount more than max_messages"""
        messages = model.all().order_by('created_at')
        messages_count = len(messages)
        if messages_count >= max_count:
            [msg.delete_model() for msg in messages[:messages_count - max_count + 1]]

    def __str__(self):
        return f'Clan {self.clan.name} | Chat: {self.name}'

    class Meta:
        unique_together = (('clan', 'name',),)
        abstract = True
