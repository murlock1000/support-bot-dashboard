from django import forms

from support_bot.models.Repositories.TicketRepository import TicketStatus
from support_bot.models.Repositories.ChatRepository import ChatStatus


class TicketFetchForm(forms.Form):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)
    
    status_choices = [(status.value, status.name) for status in TicketStatus]
    status = forms.ChoiceField(
        choices=[('', 'Select Status')] + [(status.value, status.name) for status in TicketStatus],
        required=False,
    )
    
class UserWithTicketRequest(forms.Form):
    user_id = forms.CharField()
    ticket_id = forms.CharField()
    
class TicketRequest(forms.Form):
    ticket_id = forms.IntegerField()
    
class ChatFetchForm(forms.Form):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)
    
    status_choices = [(status.value, status.name) for status in ChatStatus]
    status = forms.ChoiceField(
        choices=[('', 'Select Status')] + [(status.value, status.name) for status in ChatStatus],
        required=False,
    )
    
class UserWithChatRequest(forms.Form):
    user_id = forms.CharField()
    chat_room_id = forms.CharField()
    
class ChatRequest(forms.Form):
    chat_room_id = forms.CharField()
    
