from rest_framework import serializers, status
from rest_framework.response import Response
from Autenticacao.models import User
from dj_rest_auth.registration.serializers import RegisterSerializer

# Mapear os Campos que irão aparecer no Django REST Framework
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    # PUT
    def update(self, instance, validated_data):
        message = 'User details updated successfully.'
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
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

# Auth/Register/ // Colocar no Json a obrigatoriedade do E-Mail
class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)

    def custom_signup(self, request, user):
        user.email = self.validated_data.get('email', '')
        user.save()