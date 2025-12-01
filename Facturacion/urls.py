from django.urls import path
from Facturacion import views

urlpatterns = [
    path('crear_cita/', views.CitaCreate.as_view(), name='Crear Cita'),
    path('CitaD/<int:pk>/',views.CitaDelete.as_view(), name='Eliminar Cita'),
    path('IngresoC/',views.IngresoCreate.as_view(), name='Ingresar Ingreso'),
    path('IngresoD/<int:pk>/',views.IngresoDelete.as_view(), name='Eliminar Ingreso'),
    path('FacturaC/',views.FacturaCreate.as_view(), name='Ingresar Factura'),
    path('FacturaD/<int:pk>/',views.FacturaDelete.as_view(), name='Eliminar Factura'),
    path('Cliente/', views.cliente_dashboard, name="Cliente"),
    path('crear_cita/', views.crear_cita, name='crear_cita'),
    path('crear_ingreso/', views.crear_ingreso, name='crear_ingreso'), 
]