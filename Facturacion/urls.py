from django.urls import path, include
from Facturacion import views
from rest_framework.routers import DefaultRouter
from .views import (
    CitaViewSet,
    IngresoViewSet,
    FacturaViewSet,
    enviar_factura_view,   
)



router = DefaultRouter()
router.register(r'citas', CitaViewSet, basename='citas')
router.register(r'ingresos', IngresoViewSet, basename='ingreso')
router.register(r'facturas', FacturaViewSet, basename='factura')


urlpatterns = [
    path('Cliente/', views.cliente_dashboard, name='home'),
    path('crear_cita/', views.crear_cita, name='crear_cita'),
    path('crear_ingreso/', views.crear_ingreso, name='crear_ingreso'), 
    path('api/', include(router.urls)),
    path('factura/<int:factura_id>/descargar/', views.descargar_factura, name='descargar_factura'),
    path('factura/<int:factura_id>/enviar/', views.enviar_factura_view, name='enviar_factura'),
]
