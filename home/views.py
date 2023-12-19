from datetime import datetime, timedelta
import json
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from grpc import RpcError
from core import settings
from home.apps import store
from home.forms import TicketFetchForm, TicketRequest, UserWithTicketRequest
from home import grpc_handler
from home.helpers import ReqType, validateAjaxRequest
from home.models.repositories.DataTicketRepository import DataTicketRepository, TicketResult
from middleman.models.Repositories.StaffRepository import StaffRepository
from middleman.models.Repositories.TicketRepository import TicketRepository, TicketStatus
from django.contrib.auth.decorators import login_required


#def fetch_room_messages(request, room_id):
#    resp = grpc_handler.fetch_room_messages(room_id)
#    if isinstance(resp, RpcError):
#        response = JsonResponse({"error": resp.details()})
#        response.status_code = 500
#        return response
    
#    return JsonResponse({'success': True, "messages": resp})
        
@login_required
def unassign_staff_from_ticket(request: HttpRequest):    
    try:
        validateAjaxRequest(request, ReqType.POST)
    except Exception as e:
        response = JsonResponse({"error": str(e)})
        response.status_code = 400
        return response
    
    form = UserWithTicketRequest(request.POST)
    if form.is_valid():
        resp = grpc_handler.unassign_staff_from_ticket(form.cleaned_data["user_id"], form.cleaned_data["ticket_id"])
        if isinstance(resp, RpcError):
            response = JsonResponse({"error": resp.details()})
            response.status_code = 500
            return response
    else:
        response = JsonResponse({"error": form.errors})
        response.status_code = 400
        return response
    
    return JsonResponse({'success': True})

@login_required
def close_ticket(request):
    try:
        validateAjaxRequest(request, ReqType.POST)
    except Exception as e:
        response = JsonResponse({"error": e})
        response.status_code = 400
        return response
    
    form = TicketRequest(request.POST)
    if form.is_valid():
        resp = grpc_handler.close_ticket(form.cleaned_data["ticket_id"])
        if isinstance(resp, RpcError):
            response = JsonResponse({"error": resp.details()})
            response.status_code = 500
            return response
    else:
        response = JsonResponse({"error": form.errors})
        response.status_code = 400
        return response
    
    return JsonResponse({'success': True})

@login_required
def reopen_ticket(request):
    try:
        validateAjaxRequest(request, ReqType.POST)
    except Exception as e:
        response = JsonResponse({"error": e})
        response.status_code = 400
        return response
    
    form = TicketRequest(request.POST)
    if form.is_valid():
        resp = grpc_handler.reopen_ticket(form.cleaned_data["ticket_id"])
        if isinstance(resp, RpcError):
            response = JsonResponse({"error": resp.details()})
            response.status_code = 500
            return response
    else:
        response = JsonResponse({"error": form.errors})
        response.status_code = 400
        return response
    
    return JsonResponse({'success': True})

@login_required
def claim_ticket_for_staff(request):
    try:
        validateAjaxRequest(request, ReqType.POST)
    except Exception as e:
        response = JsonResponse({"error": e})
        response.status_code = 400
        return response
    
    form = UserWithTicketRequest(request.POST)
    if form.is_valid():
        resp = grpc_handler.claim_ticket_for_staff(form.cleaned_data["user_id"], form.cleaned_data["ticket_id"])
        if isinstance(resp, RpcError):
            response = JsonResponse({"error": resp.details()})
            response.status_code = 500
            return response
    else:
        response = JsonResponse({"error": form.errors})
        response.status_code = 400
        return response
    
    return JsonResponse({'success': True})

@login_required
def claim_ticket_for_support(request):
    try:
        validateAjaxRequest(request, ReqType.POST)
    except Exception as e:
        response = JsonResponse({"error": e})
        response.status_code = 400
        return response
    
    form = UserWithTicketRequest(request.POST)
    if form.is_valid():
        resp = grpc_handler.claim_ticket_for_support(form.cleaned_data["user_id"], form.cleaned_data["ticket_id"])
        if isinstance(resp, RpcError):
            response = JsonResponse({"error": resp.details()})
            response.status_code = 500
            return response
    else:
        response = JsonResponse({"error": form.errors})
        response.status_code = 400
        return response
    
    return JsonResponse({'success': True})

@login_required
def ticket(request, id):
    ticket_rep: TicketRepository = store.repositories.ticketRep
    data_ticket_rep = DataTicketRepository(ticket_rep)
    
    staff_rep: StaffRepository = store.repositories.staffRep
    
    ## Staff list for invites
    
    all_staff = staff_rep.get_all_staff()
    
    ## Open ticket list info
    ticket = ticket_rep.get_all_fields(id)
            # return {
            #     "id": row[0],
            #     "user_id": row[1],
            #     "ticket_room_id": row[2],
            #     "status": row[3],
            #     "ticket_name": row[4],
            #     "raised_at": row[5],
            #     "closed_at": row[6],
            # }
    
    ## Assigned staff data
    staff = ticket_rep.get_assigned_staff(id)
    staff_avatar_urls = {}
    for idx, user in enumerate(staff):
        user_id = user['user_id']
        staff_avatar_urls[user_id] = grpc_handler.fetch_avatar_url(user_id)
        if isinstance(staff_avatar_urls[user_id], RpcError):
            staff_avatar_urls[user_id] = ""
        
        if staff_avatar_urls[user_id]:
            staff[idx]['avatar_url'] = f"{settings.MATRIX_SERVER_URL}/_matrix/media/v3/thumbnail/{staff_avatar_urls[user_id][6:]}?width=48&height=48&method=crop"
    
    ## Ticket user profile
    user_avatar_url = grpc_handler.fetch_avatar_url(ticket["user_id"])
    if isinstance(user_avatar_url, RpcError):
            user_avatar_url = ""

    ticket['user_avatar_url'] = f"{settings.MATRIX_SERVER_URL}/_matrix/media/v3/thumbnail/{user_avatar_url[6:]}?width=48&height=48&method=crop"
    ticket['isClosed'] = ticket['status'] == 'closed'
    print(ticket['isClosed'])
    ticket_meta = ({
            'meta': ticket,
            'staff': staff,
        }
    )
    
    context = {
        'ticket': ticket_meta,
        'all_staff': all_staff,
    }
    return render(request, 'pages/ticket.html', context)

@login_required
def ticket_search(request):
    ticket_rep: TicketRepository = store.repositories.ticketRep
    data_ticket_rep = DataTicketRepository(ticket_rep)
    
    if request.method == 'POST':
        form = TicketFetchForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            status = form.cleaned_data['status']
            
            print(start_date, end_date, status)
            ## Open ticket list info
            open_tickets: [TicketResult] = data_ticket_rep.get_filtered_tickets(start_date, end_date, status)
            print(open_tickets)
            unique_staff = set()
            staff_avatar_urls = {}

            ticket_meta = []
            for ticket in open_tickets:
                staff = ticket_rep.get_assigned_staff(ticket.id)

                for idx, user in enumerate(staff):
                    user_id = user['user_id']
                    if user_id not in unique_staff:
                        unique_staff.add(user_id)
                        staff_avatar_urls[user_id] = grpc_handler.fetch_avatar_url(user_id)

                    if staff_avatar_urls[user_id]:
                        staff[idx]['avatar_url'] = f"{settings.MATRIX_SERVER_URL}/_matrix/media/v3/thumbnail/{staff_avatar_urls[user_id][6:]}?width=48&height=48&method=crop"

                ticket_meta.append({
                        'meta': ticket.dict(),
                        'staff': staff,
                    }
                )
    
    else:
        form = TicketFetchForm()
        ticket_meta = {}

    return render(request, 'pages/ticket_search.html', {'form': form, 'open_tickets': ticket_meta})

@login_required
def index(request):
    ticket_rep: TicketRepository = store.repositories.ticketRep
    data_ticket_rep = DataTicketRepository(ticket_rep)
    
    ## Get values for tickers
    # Get the current date at midnight
    current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Get first day of current month
    start_date = datetime(current_date.year, current_date.month, 1)
    per_month_tickets = data_ticket_rep.get_tickets_by_month(start_date, datetime.now())
    tickers = {
        "open_tickets": data_ticket_rep.get_ticket_count(TicketStatus.OPEN),
        "closed_tickets_current_month": per_month_tickets[0][1] if len(per_month_tickets) > 0 else 0,
        "closed_tickets": data_ticket_rep.get_ticket_count(TicketStatus.CLOSED),
    }
    
    ## Get values for charts

    ## Closed ticket counts per day this week
    # Closed tickets since this week
    start_date = current_date - timedelta(days=current_date.weekday())
    tickets_per_day = data_ticket_rep.get_tickets_by_day(start_date, datetime.now())
    raised_tickets_per_day = {
        'labels': ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"],
        'values': [0, 0, 0, 0, 0, 0, 0]
    }
    for day_tickets in tickets_per_day:
        day = day_tickets[0].strftime('%a')[:2]
        id = raised_tickets_per_day['labels'].index(day)
        
        raised_tickets_per_day['values'][id] = day_tickets[1]

    # Closed tickets since last year (monthly closed tickets)
    start_date = current_date - timedelta(days=365)
    tickets_per_month = data_ticket_rep.get_tickets_by_month(start_date, datetime.now())
    
    raised_tickets_per_month = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'values': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]
    }
    
    for month_tickets in tickets_per_month:
        month = month_tickets[0].strftime('%b')
        id = raised_tickets_per_month['labels'].index(month)
        raised_tickets_per_month['values'][id] = month_tickets[1]
    
    ## Cumulative ticket calculation
    total = tickers['closed_tickets']
    cumulative_tickets_per_month = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'values': []
    }
    
    cumulative_tickets_per_month['values'] = [s for s in raised_tickets_per_month['values']]
    total = total - max(cumulative_tickets_per_month['values'])
    for key, value in enumerate(cumulative_tickets_per_month['values']):
        cumulative_tickets_per_month['values'][key] = value + total
        total = cumulative_tickets_per_month['values'][key]
    
    
    charts = {
        "raised_tickets_per_day": raised_tickets_per_day,
        "raised_tickets_per_month": raised_tickets_per_month,
        "cumulative_tickets_per_month": cumulative_tickets_per_month
    }
    
    ## Open ticket list info
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
                staff_avatar_urls[user_id] = grpc_handler.fetch_avatar_url(user_id)
            
            if staff_avatar_urls[user_id]:
                staff[idx]['avatar_url'] = f"{settings.MATRIX_SERVER_URL}/_matrix/media/v3/thumbnail/{staff_avatar_urls[user_id][6:]}?width=48&height=48&method=crop"

        ticket_meta.append({
                'meta': ticket,
                'staff': staff,
            }
        )
    
    context = {
        'open_tickets': ticket_meta,
        'tickers': tickers,
        'charts': charts,
    }

    # Page from the theme
    return render(request, 'pages/index.html', context)
