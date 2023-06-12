from rest_framework import status
from rest_framework.views import exception_handler
from django.http import Http404
from Produto.API.viewsets import ProductViewSet
from Pedidos.API.viewsets import OrderViewSet
from Carrinho.API.viewsets import CartItemViewSet, CartViewSet
from Autenticacao.API.viewsets import UserViewSet

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # Erros para Autenticação
    # Login
    if (response is not None
        and response.status_code == status.HTTP_400_BAD_REQUEST
        and context['request'].path == '/auth/login/'):
        custom_response_data = {
            'error': 'Invalid credentials.',
            'errors': response.data
        }
        response.data = custom_response_data

    elif (response is not None
        and response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        and context['request'].path == '/auth/login/'):
        custom_response_data = {
                'error': 'Internal server error.'
        }
        response.data = custom_response_data

    # Logout
    if (response is not None
        and response.status_code == status.HTTP_400_BAD_REQUEST
        and context['request'].path == '/auth/logout/'):
        custom_response_data = {
            'error': 'User not logged in.',
            'errors': response.data
        }
        response.data = custom_response_data

    elif (response is not None
        and response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        and context['request'].path == '/auth/logout/'):
        custom_response_data = {
                'error': 'Internal server error.'
        }
        response.data = custom_response_data

    # Password
    if (response is not None
        and response.status_code == status.HTTP_400_BAD_REQUEST
        and context['request'].path == '/auth/password/reset/'):
        custom_response_data = {
            'error': 'Invalid password reset request.',
            'errors': response.data
        }
        response.data = custom_response_data
    
    elif (response is not None
        and response.status_code == status.HTTP_400_BAD_REQUEST
        and context['request'].path == '/auth/password/change/'):
        custom_response_data = {
            'error': 'Invalid password change request.',
            'errors': response.data
        }
        response.data = custom_response_data

    elif (response is not None
        and response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        and context['request'].path in ('/auth/password/change/',
                                        '/auth/password/reset/',
                                        'auth/password/reset/confirm/')):
        custom_response_data = {
                'error': 'Internal server error.'
        }
        response.data = custom_response_data

    # Registration
    if (response is not None
        and response.status_code == status.HTTP_400_BAD_REQUEST
        and context['request'].path in ('/auth/registration/', 
                                        '/auth/registration/verify-email/',
                                        '/auth/registration/resend-email/')):
        custom_response_data = {
            'error': 'Invalid request. Please check the provided data.',
            'errors': response.data
        }
        response.data = custom_response_data

    elif (response is not None
        and response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        and context['request'].path in ('/auth/registration/', 
                                        '/auth/registration/verify-email/',
                                        '/auth/registration/resend-email/')):
        custom_response_data = {
                'error': 'Internal server error.'
        }
        response.data = custom_response_data
    
    # User
    if (response is not None
        and response.status_code == status.HTTP_400_BAD_REQUEST
        and context['request'].path == '/auth/user/'):
        custom_response_data = {
            'error': 'Invalid request. Please check the provided data.',
            'errors': response.data
        }
        response.data = custom_response_data

    elif (response is not None
        and response.status_code == status.HTTP_401_UNAUTHORIZED
        and context['request'].path == '/auth/user/'):
        custom_response_data = {
                'error': 'Unauthorized. Authentication required.'
        }
        response.data = custom_response_data
    
    elif (response is not None
        and response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        and context['request'].path == '/auth/user/'):
        custom_response_data = {
                'error': 'Internal server error.'
        }
        response.data = custom_response_data
    
    # Erros para Items-Carrinho
    if isinstance(exc, Http404) and context['view'].__class__ == CartItemViewSet:
        custom_response_data = {
            'error': 'Cart item not found.'
        }
        response.data = custom_response_data

    elif (response is not None 
          and response.status_code == status.HTTP_400_BAD_REQUEST 
          and context['view'].__class__ == CartItemViewSet):
        custom_response_data = {
            'error': 'Invalid request. Please check the provided data.',
            'errors': response.data
        }
        response.data = custom_response_data

    elif (response is not None 
          and response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR 
          and context['view'].__class__ == CartItemViewSet):
        custom_response_data = {
            'error': 'Internal server error.'
        }
        response.data = custom_response_data    

    # Erros para Carrinho
    if isinstance(exc, Http404) and context['view'].__class__ == CartViewSet:
        custom_response_data = {
            'error': 'Cart not found.'
        }
        response.data = custom_response_data

    elif (response is not None 
          and response.status_code == status.HTTP_400_BAD_REQUEST 
          and context['view'].__class__ == CartViewSet):
        custom_response_data = {
            'error': 'Invalid request. Please check the provided data.',
            'errors': response.data
        }
        response.data = custom_response_data

    elif (response is not None 
          and response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR 
          and context['view'].__class__ == CartViewSet):
        custom_response_data = {
            'error': 'Internal server error.'
        }
        response.data = custom_response_data

    # Erros para Pedidos
    if isinstance(exc, Http404) and context['view'].__class__ == OrderViewSet:
        custom_response_data = {
            'error': 'Order not found.'
        }
        response.data = custom_response_data

    elif (response is not None 
          and response.status_code == status.HTTP_400_BAD_REQUEST 
          and context['view'].__class__ == OrderViewSet):
        custom_response_data = {
            'error': 'Invalid request. Please check the provided data.',
            'errors': response.data
        }
        response.data = custom_response_data

    elif (response is not None 
          and response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR 
          and context['view'].__class__ == OrderViewSet):
        custom_response_data = {
            'error': 'Internal server error.'
        }
        response.data = custom_response_data

    # Erros para Produtos
    if isinstance(exc, Http404) and context['view'].__class__ == ProductViewSet:
        custom_response_data = {
            'error': 'Product not found.'
        }
        response.data = custom_response_data

    elif (response is not None 
          and response.status_code == status.HTTP_400_BAD_REQUEST 
          and context['view'].__class__ == ProductViewSet):
        custom_response_data = {
            'error': 'Invalid request. Please check the provided data.',
            'errors': response.data
        }
        response.data = custom_response_data

    elif (response is not None 
          and response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR 
          and context['view'].__class__ == ProductViewSet):
        custom_response_data = {
            'error': 'Internal server error.'
        }
        response.data = custom_response_data

    # Erros para Usuarios
    if isinstance(exc, Http404) and context['view'].__class__ == UserViewSet:
        custom_response_data = {
            'error': 'User not found.'
        }
        response.data = custom_response_data

    elif (response is not None 
          and response.status_code == status.HTTP_400_BAD_REQUEST 
          and context['view'].__class__ == UserViewSet):
        custom_response_data = {
            'error': 'Invalid request. Please check the provided data.',
            'errors': response.data
        }
        response.data = custom_response_data

    elif (response is not None 
          and response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR 
          and context['view'].__class__ == UserViewSet):
        custom_response_data = {
            'error': 'Internal server error.'
        }
        response.data = custom_response_data

    return response
