from rest_framework import serializers
from Pedidos.models import Order, OrderItem
from Produto.API.serializers import ProductSerializer
from Autenticacao.models import User
from Carrinho.models import Cart
from django.db import transaction
import random, copy

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.filter(completed=False))
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'cart', 'created_at']
        read_only_fields = ['id', 'created_at']

    # Deixa a data no formato Hora:Minuto:Segundo Dia:Mes:Ano
    def get_created_at(self, obj):
        return obj.created_at.strftime('%H:%M:%S %d-%m-%Y')

    # POST
    def create(self, validated_data):
        user = validated_data.get('user')
        cart = validated_data.get('cart')

        try:
            user_obj = User.objects.get(id=user.id)
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found.')

        if cart.user != user_obj:
            raise serializers.ValidationError('The cart does not belong to the provided user.')

        with transaction.atomic():

            order = Order.objects.create(user=user_obj, cart=cart, completed=True)
            order.cart_id = cart.id  # Armazena o ID do carrinho na ordem
            order.save()

            #cart.delete()

        self._context['message'] = 'Order created successfully.'  # Adiciona a mensagem no contexto do serializer

        return order
    
    # PUT
    def update(self, instance, validated_data):
        message = 'Order updated successfully.'
        instance.cart = validated_data.get('cart', instance.cart)
        instance.save()
        self._context['message'] = message  # Armazena a mensagem no contexto do serializer
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.cart_id:
            representation = {
                'id': instance.id,
                'Cliente': instance.user.username,
                'Nota Fiscal da Compra': f'{random.randint(11, 53)}-{random.randint(1000,9999)}- \
                                        {random.randint(10000000000000,99999999999999)}- \
                                        {random.randint(0, 99)}-{random.randint(0, 999)}- \
                                        {random.randint(100000000, 999999999)}-{random.randint(0, 9)}- \
                                        {random.randint(10000000, 99999999)}-{random.randint(0, 9)}' \
                                        .replace(' ', '').replace('\n', ''),
                'Carrinho Comprado': instance.cart_id,
                'Data': representation['created_at']
            }
        if self._context['request'].accepted_renderer.format == 'json':
            if self._context['request'].method in ['POST', 'PUT']:
                return {'message': self._context['message']}
            elif self._context['request'].method == 'GET' and 'message' in self._context:
                representation['message'] = self._context['message']
        return representation