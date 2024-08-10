from django.urls import path
from chat import views

urlpatterns = [
    path("", views.ChatView.as_view(), name="chat"),
    path("list/", views.ChatListView.as_view(), name="chat_list"),
    path("history/<int:pk>/", views.ChatHistoryView.as_view(), name="history"),
]
