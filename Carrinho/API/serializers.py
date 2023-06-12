from rest_framework import serializers, status
from rest_framework.response import Response
from Carrinho.models import Cart, CartItem
from Produto.models import Product
from datetime import datetime

class CartItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    created_at = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'created_at']

    #Deixa a data no formato Hora:Minuto:Segundo Dia:Mes:Ano
    def get_created_at(self, obj):
        created_at = obj.get('created_at') if isinstance(obj, dict) else getattr(obj, 'created_at')
        if created_at is not None:
            return datetime.strftime(created_at, '%H:%M:%S %d-%m-%Y')
        return ''

    # POST
    def create(self, validated_data):
        message = 'Cart Item created successfully.'
        cart_item = CartItem.objects.create(**validated_data)
        self._context['message'] = message  # Armazena a mensagem no contexto do serializer
        return cart_item
    
    # PUT
    def update(self, instance, validated_data):
        message = 'Cart Item updated successfully.'
        instance.cart = validated_data.get('cart', instance.cart)
        instance.product = validated_data.get('product', instance.product)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        self._context['message'] = message  # Armazena a mensagem no contexto do serializer
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self._context.get('request')

        if request and request.accepted_renderer.format == 'json':
            method = request.method

            if method in ['POST', 'PUT'] and 'message' in self._context:
                return {'message': self._context['message']}
            
            if method == 'GET' and 'message' in self._context:
                representation['message'] = self._context['message']

        return representation

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']
        read_only_fields = ['id', 'created_at']

    # Deixa a data no formato Hora:Minuto:Segundo Dia:Mes:Ano
    def get_created_at(self, obj):
        return obj.created_at.strftime('%H:%M:%S %d-%m-%Y')
    
    def create(self, validated_data):
        user = self.context['request'].user
        cart = Cart.objects.create(user=user)
        return cart
    
    # POST
    def create(self, validated_data):
        message = 'Cart created successfully.'
        cart = Cart.objects.create(**validated_data)
        self._context['message'] = message  # Armazena a mensagem no contexto do serializer
        return cart
    
    # PUT
    def update(self, instance, validated_data):
        message = 'Cart updated successfully.'
        instance.user = validated_data.get('user', instance.user)
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
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']
