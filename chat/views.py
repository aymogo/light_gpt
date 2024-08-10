import os

# from openai import OpenAI
import openai
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from chat import models, serializers


client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        chat_id = request.data.get("chat_id")

        # Create a new chat or get the latest one
        chat, created = models.Chat.objects.get_or_create(
            user=request.user, pk=chat_id
        )

        user_message = request.data.get("message")

        if chat.title == "No title":
            chat.title = user_message[:30]
            chat.save()

        conversation = [
            {
                "role": message.sender,
                "content": message.content,
            }
            for message in chat.messages.all()
        ]
        conversation += [{"role": "user", "content": user_message}]

        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=conversation
        )
        bot_reply = response.choices[0].message.content

        # Save messages in the database
        models.Message.objects.create(
            chat=chat, sender="user", content=user_message
        )
        models.Message.objects.create(
            chat=chat, sender="assistant", content=bot_reply
        )

        return Response({"reply": bot_reply})


""" there should be a class for making requests for existing chats of user
it use `response.id` to save the context of the topic in chatgpt
if chat_id exists then take that chat else it None then make a new chat
"""


class ChatHistoryView(generics.ListAPIView):
    serializer_class = serializers.MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_pk = self.kwargs["pk"]
        print(chat_pk, "\n\n")
        return models.Message.objects.filter(chat__id=chat_pk)


class ChatListView(generics.ListAPIView):
    serializer_class = serializers.ChatListSerializer

    def get_object(self):
        return models.Chat.objects.filter(user=self.request.user).latest(
            "created_at"
        )
