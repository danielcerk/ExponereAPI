from rest_framework import serializers

from .models import Stock, StockMovement

class StockMovementSerializer(serializers.ModelSerializer):

    class Meta:

        model = StockMovement
        fields = '__all__'

        read_only_fields = (

            'stock', 'created_at'

        )

class StockSerializer(serializers.ModelSerializer):

    movements = StockMovementSerializer(many=True, read_only=True)
    movement = StockMovementSerializer(write_only=True, required=False)

    class Meta:
        
        model = Stock
        fields = '__all__'

        read_only_fields = (
            'product',
            'created_at',
            'updated_at'
        )

    def update(self, instance, validated_data):

        movement_data = validated_data.pop('movement', None)

        for attr, value in validated_data.items():

            setattr(instance, attr, value)

        instance.save()

        if movement_data:
            
            StockMovement.objects.create(
                stock=instance,
                **movement_data
            )

        return instance