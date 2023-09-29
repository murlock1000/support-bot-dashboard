from datetime import datetime, timedelta
from itertools import accumulate
from django.shortcuts import render
from django.http import HttpResponse
from core import settings
from home.apps import store
from home.grpc_handler import fetch_avatar_url
from home.models.repositories.DataTicketRepository import DataTicketRepository
from middleman.models.Repositories.TicketRepository import TicketRepository, TicketStatus
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    ticket_rep: TicketRepository = store.repositories.ticketRep
    data_ticket_rep = DataTicketRepository(ticket_rep)
    
    
    ## Get values for tickers
    # Get the current date at midnight
    current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Get first day of current month
    start_date = datetime(current_date.year, current_date.month, 1)
    per_month_tickets = data_ticket_rep.get_tickets_by_month(start_date)
    tickers = {
        "open_tickets": data_ticket_rep.get_ticket_count(TicketStatus.OPEN),
        "closed_tickets_current_month": per_month_tickets[0][1] if len(per_month_tickets) > 0 else 0,
        "closed_tickets": data_ticket_rep.get_ticket_count(TicketStatus.CLOSED),
    }
    
    ## Get values for charts

    ## Closed ticket counts per day this week
    # Closed tickets since this week
    start_date = current_date - timedelta(days=current_date.weekday())
    tickets_per_day = data_ticket_rep.get_tickets_by_day(start_date)
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
    tickets_per_month = data_ticket_rep.get_tickets_by_month(start_date)
    
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
    
    print(charts)
    
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
                staff_avatar_urls[user_id] = fetch_avatar_url(user_id)
            
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
