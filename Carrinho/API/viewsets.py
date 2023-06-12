from rest_framework import viewsets, status
from rest_framework.response import Response
from Carrinho.models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.permissions import IsAuthenticated

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return Cart.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    # DELETE
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        message = 'Cart deleted successfully.'
        return Response({'message': message}, status=status.HTTP_200_OK)

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart_id = self.request.data.get('cart')
        product_id = self.request.data.get('product')
        quantity = self.request.data.get('quantity')

        try:
            cart = Cart.objects.get(pk=cart_id, user=self.request.user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer.save(cart=cart, product_id=product_id, quantity=quantity)

    # DELETE
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        message = 'Cart Item deleted successfully.'
        return Response({'message': message}, status=status.HTTP_200_OK)