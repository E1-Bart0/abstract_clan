from rest_framework import serializers

from game.models import GameClanChat, GameChatRequestResource, GameChatRequestItem
from game.serializers.clan_serializers import UserSerializer
from myuser.models import User


class AllMessagesSerializer(serializers.Serializer):
    user = UserSerializer()
    type = serializers.CharField(max_length=20)
    text = serializers.CharField()
    created_at = serializers.DateTimeField()
    chat = serializers.PrimaryKeyRelatedField(queryset=GameClanChat.objects.all(), write_only=True)

    @staticmethod
    def validate_user(user):
        if hasattr(user, 'clan_member'):
            if hasattr(user.clan_member.clan, 'chats'):
                return user
            raise serializers.ValidationError('Clan do not have a chat')
        raise serializers.ValidationError('User not in clan')

    class Meta:
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    all_messages = AllMessagesSerializer(many=True, read_only=True)

    class Meta:
        model = GameClanChat
        fields = ['clan_id', 'chat_id', 'all_messages']


class SendSerializer(AllMessagesSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    type = serializers.CharField(max_length=20, required=True)
    text = serializers.CharField(required=True)
    created_at = serializers.DateTimeField(required=False)

    def to_internal_value(self, data):
        user = self.context.user
        url = self.context.path_info
        request_type = url.split('/')[-1]

        resource_data = self._get_resource_data_from(data, request_type, user)
        return super().to_internal_value(resource_data)

    @staticmethod
    def _get_resource_data_from(data, request_type, user):
        chat = user.clan_member.clan.chat if hasattr(user, 'clan_member') else None
        resource_data = {
            'user': user.id,
            'type': request_type,
            'chat': chat.chat_id if hasattr(chat, 'chat_id') else None
        }
        for item in data:
            resource_data[item] = data[item]
        if request_type != 'send_text':
            resource_data['text'] = request_type
        return resource_data

    def save(self, **kwargs):
        chat = self.validated_data.pop('chat')
        return chat.send(**self.validated_data)


class ShareSerializer(AllMessagesSerializer):
    id = serializers.IntegerField()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    type = serializers.CharField(max_length=20, required=True)
    created_at = None
    text = None

    def to_internal_value(self, data):
        request_id = self.context.GET.get('id')
        user = self.context.user
        url = self.context.path_info
        request_type = url.split('/')[-2]

        chat = user.clan_member.clan.chat if hasattr(user, 'clan_member') else None
        add_data = {
            'user': user.id,
            'type': request_type,
            'id': request_id,
            'chat': chat.chat_id if hasattr(chat, 'chat_id') else None
        }
        return super().to_internal_value(add_data)

    def validate_type(self, type):
        user = self.context.user
        request_id = self.context.GET.get('id')
        request = self._get_query_request(request_id, type)

        if request.exists():
            request = request.first()
            if request.user != user:
                return request
            raise serializers.ValidationError('You can not share you own request')
        raise serializers.ValidationError(f'Request type "{type}" with id "{request_id}" does not exist')

    @staticmethod
    def _get_query_request(request_id, request_type):
        if 'resource' in request_type:
            request = GameChatRequestResource.objects.filter(id=request_id)
        else:
            request = GameChatRequestItem.objects.filter(id=request_id)
        return request

    def save(self, **kwargs):
        chat = self.validated_data.pop('chat')
        request = self.validated_data.get('type')
        user = self.validated_data.get('user')
        print(f'{user} can interact with request {request.type} {request}')
