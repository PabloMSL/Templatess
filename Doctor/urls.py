from django.urls import  path
from  Doctor import views
from .views import DoctorCreate, DoctorDelete, HabitacionCreate, HabitacionDelete, EspecialidadCreate, EspecialidadDelete

urlpatterns = [
    path('DoctorC/', views.DoctorCreate.as_view(), name='Ingresar Doctor'),
    path('DoctorD/<int:pk>/', views.DoctorDelete.as_view(), name='Sacar Doctor'),
    path('HabitacionC/', views.HabitacionCreate.as_view(), name='Ingresar Habitacion'),
    path('HabitacionD/<int:pk>/', views.HabitacionDelete.as_view(), name='Quitar Habitacion'),
    path('EspecialidadC/', views.EspecialidadCreate.as_view(), name='Ingresar Especialidad'),
    path('EspecialidadD/<int:pk>/', views.EspecialidadDelete.as_view(), name='Quitar Especialidad')
]