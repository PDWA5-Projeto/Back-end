from rest_framework import viewsets, status
from rest_framework.response import Response
from Autenticacao.models import User
from .serializers import UserSerializer, CustomRegisterSerializer
from rest_framework.generics import GenericAPIView

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # DELETE
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        message = 'User deleted successfully.'
        return Response({'message': message}, status=status.HTTP_200_OK)

class CustomRegisterViewSet(GenericAPIView):
    serializer_class = CustomRegisterSerializer

    # Altera Mensagem do Auth/Register/
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        serializer.save(request=request)
        message = "User registration created successfully."
        return Response(
            {"message": message},
            status=status.HTTP_201_CREATED
        )
