from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

#Viewsets
from Produto.API.viewsets import ProductViewSet
from Carrinho.API.viewsets import CartViewSet, CartItemViewSet
from Autenticacao.API.viewsets import UserViewSet, CustomRegisterViewSet
from Pedidos.API.viewsets import OrderViewSet

#Swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API Documentation - E-Commerce",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Routers
router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'users', UserViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    #Administrador
    path('admin/', admin.site.urls),
    #Outras Outras
    path('', include(router.urls)),
    #Autenticação
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', CustomRegisterViewSet.as_view(), name='custom_register'),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    #Documentação Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
