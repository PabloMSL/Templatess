from django.urls import path
from Plantillas import views

urlpatterns = [
    path('home/', views.inicio, name='inicio')
]