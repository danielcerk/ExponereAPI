from django.shortcuts import get_object_or_404
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.utils import timezone
from django.conf import settings
from django.db.models.functions import TruncDate

from datetime import datetime, timedelta

from api.catalog.models import Catalog

from api.wishlist.models import Wishlist
from api.customer.models import Customer

from .models import AnalyticRoute

from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Metric,
    Dimension,
    FilterExpression,
    Filter,
    RunReportRequest,
)

import json

credentials_info = settings.GA4_CREDENTIALS
PROPERTY_ID_GA4 = settings.PROPERTY_ID_GA4

if isinstance(credentials_info, str):
    
    credentials_info = json.loads(credentials_info)

credentials = service_account.Credentials.from_service_account_info(
    credentials_info
)

client = BetaAnalyticsDataClient(credentials=credentials)

def get_catalog(id):
    
    return get_object_or_404(Catalog, user__pk=id)


def get_days_from_filter(period: str):
    periods = {
        "1d": 1,
        "7d": 7,
        "15d": 15,
        "30d": 30,
    }
    return periods.get(period, 30)

def get_route_dashboard_data(
    user_id,
    days=7,
    start_date=None,
    end_date=None
):
    catalog = get_catalog(user_id)

    analytic_route = get_object_or_404(
        AnalyticRoute,
        catalog=catalog
    )

    slug = analytic_route.slug

    if start_date and end_date:
        start = datetime.strptime(
            start_date,
            "%Y-%m-%d"
        ).date()

        end = datetime.strptime(
            end_date,
            "%Y-%m-%d"
        ).date()

        ga_start_date = start_date
        ga_end_date = end_date

    else:
        days = int(days or 7)

        end = timezone.now().date()
        start = end - timedelta(days=days - 1)

        ga_start_date = f"{days}daysAgo"
        ga_end_date = "today"

    page_filter = FilterExpression(
        filter=Filter(
            field_name="pagePath",
            string_filter=Filter.StringFilter(
                value=f"/loja/{slug}",
                match_type=Filter.StringFilter.MatchType.CONTAINS
            )
        )
    )

    return {
        "daily": get_daily_report(
            ga_start_date,
            ga_end_date,
            page_filter,
            start,
            end
        ),
        "pages": get_top_pages(
            ga_start_date,
            ga_end_date,
            page_filter
        ),
        "hours": get_peak_hours(
            ga_start_date,
            ga_end_date,
            page_filter
        ),
        "cities": get_top_cities(
            ga_start_date,
            ga_end_date,
            page_filter
        ),
        "traffic": get_traffic_sources(
            ga_start_date,
            ga_end_date,
            page_filter
        ),
    }

def get_route_chart_data(
    user_id,
    days=7,
    start_date=None,
    end_date=None
):
    catalog = get_catalog(user_id)

    analytic_route = get_object_or_404(
        AnalyticRoute,
        catalog=catalog
    )

    slug = analytic_route.slug

    if start_date and end_date:
        start = datetime.strptime(
            start_date, "%Y-%m-%d"
        ).date()

        end = datetime.strptime(
            end_date, "%Y-%m-%d"
        ).date()

        ga_start_date = start_date
        ga_end_date = end_date

    else:
        days = int(days or 7)
        end = timezone.now().date()
        start = end - timedelta(days=days - 1)

        ga_start_date = f"{days}daysAgo"
        ga_end_date = "today"

    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID_GA4}",
        dimensions=[
            Dimension(name="date"),
        ],
        metrics=[
            Metric(name="screenPageViews"),
        ],
        date_ranges=[
            DateRange(
                start_date=ga_start_date,
                end_date=ga_end_date,
            )
        ],
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="pagePath",
                string_filter=Filter.StringFilter(
                    value=f"/loja/{slug}",
                    match_type=Filter.StringFilter.MatchType.CONTAINS
                )
            )
        )
    )

    response = client.run_report(request)

    ga_data = {}

    for row in response.rows:


        raw_date = row.dimension_values[0].value

        formatted_date = f"{raw_date[6:8]}/{raw_date[4:6]}"

        ga_data[formatted_date] = {
            "views": int(row.metric_values[0].value),
        }

    chart_data = []
    current_day = start

    while current_day <= end:
        formatted_day = current_day.strftime("%d/%m")

        metrics = ga_data.get(
            formatted_day,
            {"views": 0}
        )

        chart_data.append({
            "day": formatted_day,
            "views": metrics["views"],
        })

        current_day += timedelta(days=1)

    return chart_data

def get_daily_report(
    start_date,
    end_date,
    page_filter,
    start,
    end
):

    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID_GA4}",
        dimensions=[
            Dimension(name="date")
        ],
        metrics=[
            Metric(name="screenPageViews"),
            Metric(name="activeUsers"),
            Metric(name="sessions")
        ],
        date_ranges=[
            DateRange(
                start_date=start_date,
                end_date=end_date
            )
        ],
        dimension_filter=page_filter
    )

    response = client.run_report(request)

    ga_data = {}

    for row in response.rows:

        raw = row.dimension_values[0].value

        ga_data[raw] = {
            "views": int(row.metric_values[0].value),
            "users": int(row.metric_values[1].value),
            "sessions": int(row.metric_values[2].value),
        }

    chart = []

    current = start

    while current <= end:

        raw = current.strftime("%Y%m%d")

        values = ga_data.get(raw, {
            "views": 0,
            "users": 0,
            "sessions": 0,
        })

        chart.append({
            "day": current.strftime("%d/%m"),
            "views": values["views"],
            "users": values["users"],
            "sessions": values["sessions"],
        })

        current += timedelta(days=1)

    return chart

def get_top_pages(start_date, end_date, page_filter):

    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID_GA4}",
        dimensions=[
            Dimension(name="pagePath")
        ],
        metrics=[
            Metric(name="screenPageViews")
        ],
        date_ranges=[
            DateRange(
                start_date=start_date,
                end_date=end_date
            )
        ],
        dimension_filter=page_filter,
        limit=10
    )

    response = client.run_report(request)

    return [
        {
            "page": row.dimension_values[0].value,
            "views": int(row.metric_values[0].value),
        }
        for row in response.rows
    ]

def get_peak_hours(start_date, end_date, page_filter):

    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID_GA4}",
        dimensions=[
            Dimension(name="hour")
        ],
        metrics=[
            Metric(name="screenPageViews")
        ],
        date_ranges=[
            DateRange(
                start_date=start_date,
                end_date=end_date
            )
        ],
        dimension_filter=page_filter
    )

    response = client.run_report(request)

    return [
        {
            "hour": row.dimension_values[0].value,
            "views": int(row.metric_values[0].value)
        }
        for row in response.rows
    ]

def get_top_cities(start_date, end_date, page_filter):

    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID_GA4}",
        dimensions=[
            Dimension(name="city")
        ],
        metrics=[
            Metric(name="activeUsers")
        ],
        date_ranges=[
            DateRange(
                start_date=start_date,
                end_date=end_date
            )
        ],
        dimension_filter=page_filter,
        limit=10
    )

    response = client.run_report(request)

    return [
        {
            "city": row.dimension_values[0].value,
            "users": int(row.metric_values[0].value)
        }
        for row in response.rows
    ]

def get_traffic_sources(start_date, end_date, page_filter):

    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID_GA4}",
        dimensions=[
            Dimension(name="sessionSourceMedium")
        ],
        metrics=[
            Metric(name="sessions")
        ],
        date_ranges=[
            DateRange(
                start_date=start_date,
                end_date=end_date
            )
        ],
        dimension_filter=page_filter,
        limit=10
    )

    response = client.run_report(request)

    return [
        {
            "source": row.dimension_values[0].value,
            "sessions": int(row.metric_values[0].value)
        }
        for row in response.rows
    ]

def apply_date_filter(qs, start_date=None, end_date=None, days=None):

    if days:

        start_date = timezone.now() - timedelta(days=days)

    if start_date:

        qs = qs.filter(created_at__gte=start_date)

    if end_date:

        qs = qs.filter(created_at__lte=end_date)

    return qs

def get_all_customer(id, start_date=None, end_date=None, days=None):

    cat = get_catalog(id)

    qs = Customer.objects.filter(

        catalog=cat

    )

    qs = apply_date_filter(qs, start_date, end_date, days)

    return qs.count()

def get_all_wishlist(id, start_date=None, end_date=None, days=None):

    cat = get_catalog(id)

    qs = Wishlist.objects.filter(
        product__catalog=cat,
        is_active=True
    )

    qs = apply_date_filter(qs, start_date, end_date, days)

    return qs.values('session_key').distinct().count()