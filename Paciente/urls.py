from django.urls import path
from Paciente import views

urlpatterns = [
    path('PacienteC/', views.PacienteCreate.as_view(), name='Ingresar paciente'),
    path('PacienteD/<int:pk>/',views.PacienteDelete.as_view(), name='Despachar Paciente'),
    path('HistorialC/',views.HistorialCreate.as_view(), name='Crear Historial Medico'),
    path('HistorialD/<int:pk>/',views.HistorialDelete.as_view(), name='Eliminar Historial Medico'),
    path('dashboard/', views.paciente_dashboard, name='paciente_dashboard'),
    path('registro/', views.registro, name='registro'),
]