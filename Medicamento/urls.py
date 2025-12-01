from django.urls import path
from Medicamento import views

urlpatterns = [
    path('MedicamentoC/', views.MedicamentoCreate.as_view(), name='Ingresar medicamento'),
    path('MedicamentoD/<int:pk>/',views.MedicamentoDelete.as_view(), name='Sacar Medicamento'),
    path('RecetaC/',views.RecetaCreate.as_view(), name='Crear Receta'),
    path('RecetaD/<int:pk>/',views.RecetaDelete.as_view(), name='Eliminar Receta')
]