import logging
from django.shortcuts import render
from django.http import HttpResponse
from home.apps import store
from middleman.models.Repositories.TicketRepository import TicketRepository

# Create your views here.

def index(request):

    ticket_rep: TicketRepository = store.repositories.ticketRep
        
    open_tickets = ticket_rep.get_open_tickets()
    
    ticket_meta = []
    for ticket in open_tickets:
        ticket_id = ticket['id']
        ticket_meta.append({
                'meta': ticket,
                'staff': ticket_rep.get_assigned_staff(ticket_id),
            }
        )
    
    context = {
        'open_tickets': ticket_meta,
    }

    # Page from the theme
    return render(request, 'pages/index.html', context)
