from rest_framework import serializers
from chat import models


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = ["sender", "content", "created_at"]


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Chat
        fields = ["id", "user", "created_at", "messages"]


class ChatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chat
        fields = ["id", "title", "user", "created_at"]