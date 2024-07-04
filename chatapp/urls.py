from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('direct/<str:username>/', views.directs, name='directs'),
    path('send/', views.sendDirect, name="send-direct"),
    path('delete-direct/<int:pk>/', views.deleteDirect, name="delete-direct"),
    path('search/', views.UserSearch, name="search"),
    path('edit-message/<int:message_id>/', views.edit_message, name='edit-message'),
    
    # Room
    path('create-room/', views.createRoom, name="create-room"),
    path('chat-rooms', views.chat_list, name="chat-list"),
    path('chat-room/<int:pk>/', views.RoomView, name="chat-room"),
    path('join-room/<int:pk>/', views.join_room, name="join-room"),
    path('leave-room/<int:pk>/', views.leave_room, name="leave-room"),
    path('send-message/<int:pk>/', views.sendMsg, name="send-msg"),
]
