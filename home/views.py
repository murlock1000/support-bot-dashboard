from datetime import datetime, timedelta
import json
from django.shortcuts import redirect, render
from django.http import HttpRequest, JsonResponse
from grpc import RpcError
from core import settings
from home.apps import store
from home.forms import TicketFetchForm, TicketRequest, UserWithTicketRequest
from home import grpc_handler
from home.helpers import ReqType, validateAjaxRequest, format_time_difference
from home.models.repositories.DataTicketRepository import DataTicketRepository, TicketResult
from support_bot.models.Repositories.StaffRepository import StaffRepository
from support_bot.models.Repositories.TicketRepository import TicketRepository, TicketStatus
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
def delete_ticket_room(request):
    try:
        validateAjaxRequest(request, ReqType.POST)
    except Exception as e:
        response = JsonResponse({"error": e})
        response.status_code = 400
        return response
    
    form = TicketRequest(request.POST)
    if form.is_valid():
        resp = grpc_handler.delete_ticket_room(form.cleaned_data["ticket_id"])
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
def staff(request, user_id):
    ticket_rep: TicketRepository = store.repositories.ticketRep
    data_ticket_rep = DataTicketRepository(ticket_rep)
    staff_rep: StaffRepository = store.repositories.staffRep
    
    ## Check staff exists
    staff_id = staff_rep.get_staff(user_id)
    
    if staff_id is None:
        return redirect('index')
    
    ## Assigned staff data
    staff = {
        'user_id': staff_id
    }
    
    staff_avatar_url = ""
    staff_avatar_url = grpc_handler.fetch_avatar_url(staff_id)
    if staff_avatar_url:
        staff['avatar_url'] = f"{settings.MATRIX_SERVER_URL}/_matrix/media/v3/thumbnail/{staff_avatar_url[6:]}?width=48&height=48&method=crop"
    
    
    ## Ticket blocks
    if request.method == 'POST':
        form = TicketFetchForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            status = form.cleaned_data['status']
            
            ## Open ticket list info
            open_tickets: [TicketResult] = data_ticket_rep.get_filtered_staff_tickets(start_date, end_date, status, staff_id)
            unique_staff = set()
            staff_avatar_urls = {}

            search_ticket_meta = []
            for ticket in open_tickets:
                assigned_staff = ticket_rep.get_assigned_staff(ticket.id)

                for idx, user in enumerate(assigned_staff):
                    user_id = user['user_id']
                    if user_id not in unique_staff:
                        unique_staff.add(user_id)
                        staff_avatar_urls[user_id] = grpc_handler.fetch_avatar_url(user_id)

                    if staff_avatar_urls[user_id]:
                        assigned_staff[idx]['avatar_url'] = f"{settings.MATRIX_SERVER_URL}/_matrix/media/v3/thumbnail/{staff_avatar_urls[user_id][6:]}?width=48&height=48&method=crop"

                search_ticket_meta.append({
                        'meta': ticket.dict(),
                        'staff': assigned_staff,
                    }
                )
    
    else:
        form = TicketFetchForm()
        search_ticket_meta = {}
    
    ## Info block
    # Get the current date at midnight
    current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Get first day of current month
    start_date = datetime(current_date.year, current_date.month, 1)
    current_month_closed_tickets = data_ticket_rep.get_staff_closed_tickets_by_month(start_date, datetime.now(), staff_id)
    tickers = {
        "open_tickets": data_ticket_rep.get_staff_ticket_count(TicketStatus.OPEN, staff_id),
        "closed_tickets_current_month": current_month_closed_tickets[0][1] if len(current_month_closed_tickets) > 0 else 0,
        "closed_tickets": data_ticket_rep.get_staff_ticket_count(TicketStatus.CLOSED, staff_id),
    }
    
    ## Get values for charts
    ## Closed ticket counts per day this week
    # Closed tickets since this week
    start_date = current_date - timedelta(days=current_date.weekday())
    tickets_per_day = data_ticket_rep.get_staff_opened_tickets_by_day(start_date, datetime.now(), staff_id)
    raised_tickets_per_day = {
        'labels': ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"],
        'values': [0, 0, 0, 0, 0, 0, 0]
    }
    for day_tickets in tickets_per_day:
        if day_tickets[0] is not None:
            day = day_tickets[0].strftime('%a')[:2]
            id = raised_tickets_per_day['labels'].index(day)
        
            raised_tickets_per_day['values'][id] = day_tickets[1]
    
    # Closed tickets since last year (monthly closed tickets)
    start_date = datetime(current_date.year-1, current_date.month+1, 1)
    raised_tickets_per_month_data = data_ticket_rep.get_staff_opened_tickets_by_month(start_date, datetime.now(), staff_id)
    
    raised_tickets_per_month = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'values': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]
    }
    
    for month_tickets in raised_tickets_per_month_data:
        if month_tickets[0] != None: 
            month = month_tickets[0].strftime('%b')
            id = raised_tickets_per_month['labels'].index(month)
            raised_tickets_per_month['values'][id] = month_tickets[1]
    
    ## Cumulative ticket calculation
    total = tickers['closed_tickets'] + tickers['open_tickets']
    cumulative_tickets_per_month = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'values': [0 for x in range(12)]
    }
    
    for month_id in range(datetime.now().month-1, -len(cumulative_tickets_per_month['labels'])+datetime.now().month-1, -1):
        cumulative_tickets_per_month['values'][month_id] = total
        total -= raised_tickets_per_month['values'][month_id]
    
    charts = {
        "raised_tickets_per_day": raised_tickets_per_day,
        "raised_tickets_per_month": raised_tickets_per_month,
        "cumulative_tickets_per_month": cumulative_tickets_per_month
    }
    
    ## Open ticket list info
    open_tickets = data_ticket_rep.get_staff_info_tickets(staff_id)
    
    unique_staff = set()
    staff_avatar_urls = {}
    
    ticket_meta = []
    for ticket in open_tickets:
        ticket_id = ticket['id']
        
        # Format time open
        timeOpen = "-"
        raisedAt = ticket['raised_at']
        if raisedAt is not None:
            timeOpen = format_time_difference((datetime.now() - raisedAt).total_seconds())
            ticket['time_open'] = timeOpen
            
        assigned_staff = ticket_rep.get_assigned_staff(ticket_id)
        
        for idx, user in enumerate(assigned_staff):
            user_id = user['user_id']
            if user_id not in unique_staff:
                unique_staff.add(user_id)
                staff_avatar_urls[user_id] = grpc_handler.fetch_avatar_url(user_id)
            
            if staff_avatar_urls[user_id]:
                assigned_staff[idx]['avatar_url'] = f"{settings.MATRIX_SERVER_URL}/_matrix/media/v3/thumbnail/{staff_avatar_urls[user_id][6:]}?width=48&height=48&method=crop"

        ticket_meta.append({
                'meta': ticket,
                'staff': assigned_staff,
            }
        )
    
    context = {
        'staff': staff,
        'open_tickets': ticket_meta,
        'tickers': tickers,
        'charts': charts,
        'form': form,
        'search_tickets': search_ticket_meta,
    }
    
    print(context)
    return render(request, 'pages/staff.html', context)

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
    current_month_closed_tickets = data_ticket_rep.get_closed_tickets_by_month(start_date, datetime.now())
    tickers = {
        "open_tickets": data_ticket_rep.get_ticket_count(TicketStatus.OPEN),
        "closed_tickets_current_month": current_month_closed_tickets[0][1] if len(current_month_closed_tickets) > 0 else 0,
        "closed_tickets": data_ticket_rep.get_ticket_count(TicketStatus.CLOSED),
    }
    
    ## Get values for charts

    ## Closed ticket counts per day this week
    # Closed tickets since this week
    start_date = current_date - timedelta(days=current_date.weekday())
    tickets_per_day = data_ticket_rep.get_opened_tickets_by_day(start_date, datetime.now())
    raised_tickets_per_day = {
        'labels': ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"],
        'values': [0, 0, 0, 0, 0, 0, 0]
    }
    for day_tickets in tickets_per_day:
        if day_tickets[0] is not None:
            day = day_tickets[0].strftime('%a')[:2]
            id = raised_tickets_per_day['labels'].index(day)
        
            raised_tickets_per_day['values'][id] = day_tickets[1]

    # Closed tickets since last year (monthly closed tickets)
    start_date = datetime(current_date.year-1, current_date.month+1, 1)
    raised_tickets_per_month_data = data_ticket_rep.get_opened_tickets_by_month(start_date, datetime.now())
    
    raised_tickets_per_month = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'values': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]
    }
    
    for month_tickets in raised_tickets_per_month_data:
        if month_tickets[0] != None: 
            month = month_tickets[0].strftime('%b')
            id = raised_tickets_per_month['labels'].index(month)
            raised_tickets_per_month['values'][id] = month_tickets[1]
    
    ## Cumulative ticket calculation
    total = tickers['closed_tickets'] + tickers['open_tickets']
    cumulative_tickets_per_month = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'values': [0 for x in range(12)]
    }
    
    for month_id in range(datetime.now().month-1, -len(cumulative_tickets_per_month['labels'])+datetime.now().month-1, -1):
        cumulative_tickets_per_month['values'][month_id] = total
        total -= raised_tickets_per_month['values'][month_id]
    
    charts = {
        "raised_tickets_per_day": raised_tickets_per_day,
        "raised_tickets_per_month": raised_tickets_per_month,
        "cumulative_tickets_per_month": cumulative_tickets_per_month
    }
    
    ## Open ticket list info
    open_tickets = data_ticket_rep.get_homepage_tickets()
    
    unique_staff = set()
    staff_avatar_urls = {}
    
    ticket_meta = []
    for ticket in open_tickets:
        ticket_id = ticket['id']
        
        # Format time open
        timeOpen = "-"
        raisedAt = ticket['raised_at']
        if raisedAt is not None:
            timeOpen = format_time_difference((datetime.now() - raisedAt).total_seconds())
            ticket['time_open'] = timeOpen
            
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
