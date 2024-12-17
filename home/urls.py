from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ticket_search/', views.ticket_search, name='ticket_search'),
    path('chat_search/', views.chat_search, name='chat_search'),
    path('ticket/<int:id>/', views.ticket, name='ticket'),
    path('chat/<str:chat_room_id>/', views.chat, name='chat'),
    path('staff/<str:user_id>/', views.staff, name='staff'),
    path('ajax/unassign_staff_from_ticket/', views.unassign_staff_from_ticket, name='unassign_staff_from_ticket'),
    path('ajax/unassign_staff_from_chat/', views.unassign_staff_from_chat, name='unassign_staff_from_chat'),
    path('ajax/close_ticket/', views.close_ticket, name='close_ticket'),
    path('ajax/close_chat/', views.close_chat, name='close_chat'),
    path('ajax/reopen_ticket/', views.reopen_ticket, name='reopen_ticket'),
    path('ajax/delete_ticket_room/', views.delete_ticket_room, name='delete_ticket_room'),
    path('ajax/delete_chat_room/', views.delete_chat_room, name='delete_chat_room'),
    path('ajax/claim_ticket_for_staff/', views.claim_ticket_for_staff, name='claim_ticket_for_staff'),
    path('ajax/claim_ticket_for_support/', views.claim_ticket_for_support, name='claim_ticket_for_support'),
    path('ajax/claim_chat_for_staff/', views.claim_chat_for_staff, name='claim_chat_for_staff'),
    path('ajax/claim_chat_for_support/', views.claim_chat_for_support, name='claim_chat_for_support'),
    path('ajax/fetch_ticket_messages/', views.fetch_ticket_messages, name='fetch_ticket_messages'),
]
