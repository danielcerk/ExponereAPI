from rest_framework import serializers

from .utils import (
    get_all_customer,
    get_all_wishlist,
    get_route_chart_data,
)

from api.financial.serializers import FinancialSerializer

class AnalyticSerializer(serializers.Serializer):

    customer = serializers.SerializerMethodField()
    wishlist = serializers.SerializerMethodField()
    financial = serializers.SerializerMethodField()
    route_chart = serializers.SerializerMethodField()

    def get_filters(self):

        return {
            "start_date": self.context.get("start_date"),
            "end_date": self.context.get("end_date"),
            "days": self.context.get("days"),
        }

    def get_customer(self, obj):

        return get_all_customer(obj.id, **self.get_filters())

    def get_wishlist(self, obj):

        return get_all_wishlist(obj.id, **self.get_filters())

    def get_financial(self, obj):

        serializer = FinancialSerializer(
            obj,
            context=self.context
        )

        return serializer.data

    def get_route_chart(self, obj):
        
        return get_route_chart_data(
            user_id=obj.user.id,
            days=self.context.get("days"),
            start_date=self.context.get("start_date"),
            end_date=self.context.get("end_date"),
        )