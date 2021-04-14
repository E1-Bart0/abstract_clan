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
    def requests_resource(self):
        return self.requests_resource

    @property
    def requests_item(self):
        return self.requests_item

    @property
    def notifications(self):
        return self.notifications

    @property
    def all_messages(self):
        text_messages = self.messages.all()
        resource_request = self.requests_resource.all()
        requests_item = self.requests_item.all()
        notifications = self.notifications.all()
        all_msgs = text_messages.union(resource_request, requests_item, notifications)
        return all_msgs

    def send(self, user, request_type, **kwargs):
        model = {
            'message': self.messages,
            'requests_resource': self.requests_resource,
            'requests_item': self.requests_item,
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
            [msg.delete() for msg in messages[:messages_count - max_count + 1]]

    def __str__(self):
        return f'Clan {self.clan.name} | Chat: {self.name}'

    class Meta:
        unique_together = (('clan', 'name',),)
        abstract = True
