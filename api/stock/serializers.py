from rest_framework.serializers import ModelSerializer

from .models import Stock, StockMovement

class StockMovementSerializer(ModelSerializer):

    class Meta:

        model = StockMovement
        fields = '__all__'

class StockSerializer(ModelSerializer):

    stock_mov = StockMovementSerializer()

    class Meta:

        model = Stock
        fields = '__all__'