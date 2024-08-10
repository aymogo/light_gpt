from django.db import models

from django.contrib.auth.models import User


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, default="No title")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Message(models.Model):
    chat = models.ForeignKey(
        Chat, related_name="messages", on_delete=models.CASCADE
    )
    sender = models.CharField(max_length=16)  # 'user' or 'bot'
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} @ {self.created_at}"
