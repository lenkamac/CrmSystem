from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncDate
from lead.models import Lead
from client.models import Client
from datetime import timedelta
from django.utils import timezone
import json


app_name = 'dashboard'


# Create your views here.
@login_required
def dashboard(request):
    lead_count = Lead.objects.filter(created_by=request.user).count()
    client_count = Client.objects.filter(created_by=request.user).count()
    latest_leads = Lead.objects.filter(created_by=request.user).order_by('-created_at')[:5]
    latest_clients = Client.objects.filter(created_by=request.user).order_by('-created_at')[:5]

    # Get time period filter from request
    time_period = request.GET.get('period', 'all')

    # Calculate date range based on selected period
    today = timezone.now()
    if time_period == '7days':
        start_date = today - timedelta(days=7)
    elif time_period == '30days':
        start_date = today - timedelta(days=30)
    elif time_period == '90days':
        start_date = today - timedelta(days=90)
    elif time_period == '6months':
        start_date = today - timedelta(days=180)
    elif time_period == '1year':
        start_date = today - timedelta(days=365)
    else:  # 'all'
        start_date = None

    # Generate leads over time data for the graph
    leads_query = Lead.objects.filter(created_by=request.user)

    # Apply date filter if not 'all'
    if start_date:
        leads_query = leads_query.filter(created_at__gte=start_date)

    leads_over_time = (
        leads_query
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    # Generate clients over time data
    clients_query = Client.objects.filter(created_by=request.user)
    if start_date:
        clients_query = clients_query.filter(created_at__gte=start_date)

    clients_over_time = (
        clients_query
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    # Prepare data for Chart.js
    lead_dates = [item['date'].strftime('%Y-%m-%d') for item in leads_over_time]
    lead_counts = [item['count'] for item in leads_over_time]

    # Prepare data for Chart.js - Clients
    client_dates = [item['date'].strftime('%Y-%m-%d') for item in clients_over_time]
    client_counts = [item['count'] for item in clients_over_time]

    # Combine all unique dates
    all_dates = sorted(list(set(lead_dates + client_dates)))

    # Create dictionaries for easy lookup
    lead_dict = dict(zip(lead_dates, lead_counts))
    client_dict = dict(zip(client_dates, client_counts))

    # Fill in missing dates with 0
    lead_counts_filled = [lead_dict.get(date, 0) for date in all_dates]
    client_counts_filled = [client_dict.get(date, 0) for date in all_dates]

    context = {
        'lead_count': lead_count,
        'client_count': client_count,
        'latest_leads': latest_leads,
        'latest_clients': latest_clients,
        'chart_dates': json.dumps(all_dates),
        'lead_counts': json.dumps(lead_counts_filled),
        'client_counts': json.dumps(client_counts_filled),
        'selected_period': time_period,
    }

    return render(request, 'dashboard/dashboard.html', context)