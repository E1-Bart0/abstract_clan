from rest_framework import serializers

from game.models import GameClanChat, GameChatRequestResource, GameChatRequestItem
from game.serializers.clan_serializers import UserSerializer
from myuser.models import User


class AllMessagesSerializer(serializers.Serializer):
    user = UserSerializer()
    type = serializers.CharField(max_length=20)
    text = serializers.CharField()
    created_at = serializers.DateTimeField()

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

        add_data = {
            'user': user.id,
            'type': request_type,
        }

        for item in data:
            add_data[item] = data[item]

        if request_type != 'send_text':
            add_data['text'] = request_type

        return super().to_internal_value(add_data)

    def validate_user(self, user):
        if hasattr(user, 'clan_member') and hasattr(user.clan_member.clan, 'chats'):
            return user
        raise serializers.ValidationError('User not in clan')

    def save(self, **kwargs):
        user = self.validated_data.get('user')
        return user.clan_member.clan.chat.send(**self.validated_data)


class ShareSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    type = serializers.CharField(max_length=20, required=True)

    def to_internal_value(self, data):
        request_id = self.context.GET.get('id')
        user = self.context.user

        url = self.context.path_info
        request_type = url.split('/')[-2]

        add_data = {
            'user': user.id,
            'type': request_type,
            'id': request_id,
        }
        return super().to_internal_value(add_data)

    def validate_user(self, user):
        if hasattr(user, 'clan_member') and hasattr(user.clan_member.clan, 'chats'):
            return user
        raise serializers.ValidationError('User not in clan')

    def validate_type(self, type):
        user = self.context.user
        request_id = self.context.GET.get('id')
        if 'resource' in type:
            request = GameChatRequestResource.objects.filter(id=request_id)
        else:
            request = GameChatRequestItem.objects.filter(id=request_id)

        if request.exists():
            request = request.first()
            if request.user != user:
                return request
            raise serializers.ValidationError('You can not share you own request')
        raise serializers.ValidationError(f'Request type "{type}" with id "{request_id}" does not exist')

    def save(self, **kwargs):
        request = self.validated_data.get('type')
        user = self.validated_data.get('user')
        print(f'{user} can interact with request {request.type} {request}')
