from rest_framework import viewsets, status
from Produto.models import Product
from rest_framework.response import Response
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # DELETE
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        message = 'Product deleted successfully.'
        return Response({'message': message}, status=status.HTTP_200_OK)