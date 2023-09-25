import logging
from django.shortcuts import render
from django.http import HttpResponse
import grpc
from core import settings
from home.apps import store, channel
from middleman.models.Repositories.TicketRepository import TicketRepository

from proto import support_bot_pb2, support_bot_pb2_grpc

# Create your views here.

def _fetch_avatar_url(user_id):
    stub = support_bot_pb2_grpc.MetaHandlerStub(channel)
    request = support_bot_pb2.AvatarURLRequest(user_id=user_id)
    
    try:
        response = stub.FetchAvatarURL(request)
    except grpc.RpcError as rpc_error:
        logging.error("Received error: %s", rpc_error)
        return None
    else:
        #if response.status_code:
        #    logging.error("Received error message: %s", response)
        return response.avatar_url

def index(request):

    ticket_rep: TicketRepository = store.repositories.ticketRep
        
    open_tickets = ticket_rep.get_open_tickets()
    
    
    unique_staff = set()
    staff_avatar_urls = {}
    
    ticket_meta = []
    for ticket in open_tickets:
        ticket_id = ticket['id']
        staff = ticket_rep.get_assigned_staff(ticket_id)
        
        for idx, user in enumerate(staff):
            user_id = user['user_id']
            if user_id not in unique_staff:
                unique_staff.add(user_id)
                staff_avatar_urls[user_id] = _fetch_avatar_url(user_id)
            
            if staff_avatar_urls[user_id]:
                staff[idx]['avatar_url'] = f"{settings.MATRIX_SERVER_URL}/_matrix/media/v3/thumbnail/{staff_avatar_urls[user_id][6:]}?width=48&height=48&method=crop"

        ticket_meta.append({
                'meta': ticket,
                'staff': staff,
            }
        )
    
    context = {
        'open_tickets': ticket_meta,
    }

    # Page from the theme
    return render(request, 'pages/index.html', context)
