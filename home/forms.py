from django import forms

from middleman.models.Repositories.TicketRepository import TicketStatus


class TicketFetchForm(forms.Form):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    
    status_choices = [(status.value, status.name) for status in TicketStatus]
    status = forms.ChoiceField(
        choices=[('', 'Select Status')] + [(status.value, status.name) for status in TicketStatus],
        required=False,
    )