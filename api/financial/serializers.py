from rest_framework import serializers

from .utils import (
    revenue_catalog,
    profit_catalog,
    best_selling_product,
    worst_selling_product
)


class FinancialSerializer(serializers.Serializer):

    revenue = serializers.SerializerMethodField()
    best_product = serializers.SerializerMethodField()
    worst_product = serializers.SerializerMethodField()

    def get_filters(self):
        
        return {
            'start_date': self.context.get('start_date'),
            'end_date': self.context.get('end_date'),
            'days': self.context.get('days'),
        }

    def get_revenue(self, obj):

        return revenue_catalog(obj.id, **self.get_filters())

    def get_best_product(self, obj):

        return best_selling_product(obj.id, **self.get_filters())

    def get_worst_product(self, obj):

        return worst_selling_product(obj.id, **self.get_filters())