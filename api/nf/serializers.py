from rest_framework import serializers

from .models import NF

from api.cloudinary_utils import ( 
    
    upload_to_cloudinary_nf,
    delete_from_cloudinary_nf

)

class NFSerializer(serializers.ModelSerializer):

    file = serializers.FileField(write_only=True, required=False)

    class Meta:

        model = NF
        fields = '__all__'
        read_only_fields = ('id', 'order', 'created_at', 'updated_at', 'file_url')

    def validate_access_key(self, value):

        if value:

            value = value.strip()

            if len(value) != 44 or not value.isdigit():

                raise serializers.ValidationError("Chave de acesso inválida.")

        return value

    def validate_number(self, value):

        if value:

            return value.strip()
        
        return value

    def validate(self, data):

        order = data.get("order", getattr(self.instance, "order", None))

        if NF.objects.filter(order=order).exclude(
            pk=self.instance.pk if self.instance else None
        ).exists():
            
            raise serializers.ValidationError({
                "order": "Este pedido já possui uma nota fiscal."
            })

        return data

    def create(self, validated_data):

        file = validated_data.pop("file", None)

        if file:

            validated_data["file_url"] = upload_to_cloudinary_nf(file)

        return super().create(validated_data)

    def update(self, instance, validated_data):

        file = validated_data.pop("file", None)

        remove_file = self.initial_data.get("file") in [None, "", "null"]

        if file:

            if instance.file_url:

                delete_from_cloudinary_nf(instance.file_url)

            validated_data["file_url"] = upload_to_cloudinary_nf(file)

        elif remove_file:

            if instance.file_url:
                
                delete_from_cloudinary_nf(instance.file_url)

            validated_data["file_url"] = None

        return super().update(instance, validated_data)