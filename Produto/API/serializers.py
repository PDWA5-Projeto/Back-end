from rest_framework import serializers, status
from Produto.models import Product
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price']
        read_only_fields = ['id']

    # POST
    def create(self, validated_data):
        message = 'Product created successfully.'
        product = Product.objects.create(**validated_data)
        self._context['message'] = message  # Armazena a mensagem no contexto do serializer
        return product
    
    # PUT
    def update(self, instance, validated_data):
        message = 'Product updated successfully.'
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        self._context['message'] = message  # Armazena a mensagem no contexto do serializer
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self._context['request'].accepted_renderer.format == 'json':
            if self._context['request'].method in ['POST', 'PUT']:
                return {'message': self._context['message']}
            elif self._context['request'].method == 'GET' and 'message' in self._context:
                representation['message'] = self._context['message']
        return representation