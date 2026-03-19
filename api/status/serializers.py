from rest_framework import serializers

import json

from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Metric,
    RunReportRequest,
)

from django.db.models import Count
from django.db.models.functions import TruncDate
from django.contrib.auth import get_user_model
from datetime import date, datetime, timedelta

from django.conf import settings

User = get_user_model()

credentials_info = settings.GA4_CREDENTIALS
PROPERTY_ID_GA4 = settings.PROPERTY_ID_GA4

credentials = service_account.Credentials.from_service_account_info(

    credentials_info

)

client = BetaAnalyticsDataClient(credentials=credentials)

def all_views_ga4(property_id):

    request = RunReportRequest(
        property=f"properties/{property_id}",
        metrics=[Metric(name="screenPageViews")],
        date_ranges=[DateRange(start_date="2026-01-01", end_date="today")],
    )

    response = client.run_report(request)

    total_views = 0

    for row in response.rows:

        total_views += int(row.metric_values[0].value)

    return total_views

class StatusAnalyticSerializer(serializers.Serializer):

    users_last_7_days = serializers.SerializerMethodField()
    total_views = serializers.SerializerMethodField()

    def get_users_last_7_days(self, obj):

        today = date.today()
        seven_days_before = today - timedelta(days=7)

        return User.objects.filter(
            created_at__gte=seven_days_before
        ).count()

    def get_total_views(self, obj):

        return all_views_ga4(property_id=PROPERTY_ID_GA4)
