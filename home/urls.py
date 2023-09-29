from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ticket_search/', views.ticket_search, name='ticket_search'),
]
