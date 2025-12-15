from django.shortcuts import  render, redirect, get_object_or_404
from .models import Doctor, Habitacion, Especialidad
from .serializers import DoctorSerializer, HabitacionSerializer, EspecialidadSerializer
from rest_framework import generics
from .forms import EspecialidadForm, HabitacionForm

class DoctorCreate(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class DoctorDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class HabitacionCreate(generics.ListCreateAPIView):
    queryset = Habitacion.objects.all()
    serializer_class = HabitacionSerializer

class HabitacionDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Habitacion.objects.all()
    serializer_class = HabitacionSerializer

class EspecialidadCreate(generics.ListCreateAPIView):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer

class EspecialidadDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
    

def base(request):
    doctores = Doctor.objects.all()
    contexto = {
        'nombre_pagina': "Hospital Moderno",
        'abierto': True,
        'doctores': doctores,
        'imagenes': [
            'logo.jpg',
            'doctor.jpg',
            'hospital.jpg'
        ]
    }
    return render(request, 'Doctor/Doctor.html', contexto)


def admin_dashboard(request):
    especialidades = Especialidad.objects.all()
    habitaciones = Habitacion.objects.all()

    contexto = {
        'especialidades': especialidades,
        'habitaciones': habitaciones,
    }
    return render(request, 'Doctor/AdminDashboard.html', contexto)

# Agregar o editar especialidad
def especialidad_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = EspecialidadForm()
        else:
            especialidad = get_object_or_404(Especialidad, pk=id)
            form = EspecialidadForm(instance=especialidad)
        return render(request, "Admin/especialidad_form.html", {'form': form})
    else:
        if id == 0:
            form = EspecialidadForm(request.POST)
        else:
            especialidad = get_object_or_404(Especialidad, pk=id)
            form = EspecialidadForm(request.POST, instance=especialidad)
        if form.is_valid():
            form.save()
        return redirect('admin_dashboard')

# Eliminar especialidad
def especialidad_delete(request, id):
    especialidad = get_object_or_404(Especialidad, pk=id)
    especialidad.delete()
    return redirect('admin_dashboard')

# Lo mismo para Habitaciones
def habitacion_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = HabitacionForm()
        else:
            habitacion = get_object_or_404(Habitacion, pk=id)
            form = HabitacionForm(instance=habitacion)
        return render(request, "Admin/habitacion_form.html", {'form': form})
    else:
        if id == 0:
            form = HabitacionForm(request.POST)
        else:
            habitacion = get_object_or_404(Habitacion, pk=id)
            form = HabitacionForm(request.POST, instance=habitacion)
        if form.is_valid():
            form.save()
        return redirect('admin_dashboard')

def habitacion_delete(request, id):
    habitacion = get_object_or_404(Habitacion, pk=id)
    habitacion.delete()
    return redirect('admin_dashboard')