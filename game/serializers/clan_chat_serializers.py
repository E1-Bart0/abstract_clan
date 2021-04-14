from rest_framework import serializers

from game.models import (
    GameChatRequestItem,
    GameChatRequestResource,
    GameChatTextMessage,
    GameChatNotification,
    GameClanChat,
)


class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameChatNotification
        fields = '__all__'


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameChatTextMessage
        fields = '__all__'


class ResourceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameChatRequestResource
        fields = '__all__'


class ItemRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameChatRequestItem
        fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):
    resource_request