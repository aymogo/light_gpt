from django.contrib import admin

from chat import models


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "created_at")


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("chat", "sender", "content", "created_at")
