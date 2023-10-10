from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ticket_search/', views.ticket_search, name='ticket_search'),
    path('ticket/<int:id>/', views.ticket, name='ticket'),
    path('ajax/unassign_staff_from_ticket/', views.unassign_staff_from_ticket, name='unassign_staff_from_ticket'),
    path('ajax/close_ticket/', views.close_ticket, name='close_ticket'),
    path('ajax/reopen_ticket/', views.reopen_ticket, name='reopen_ticket'),
    path('ajax/claim_ticket_for_staff/', views.claim_ticket_for_staff, name='claim_ticket_for_staff'),
    path('ajax/claim_ticket_for_support/', views.claim_ticket_for_support, name='claim_ticket_for_support'),
]
