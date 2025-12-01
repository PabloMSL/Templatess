from django.shortcuts import render
from .models import Paciente, HistorialMedico
from .serializers import PacienteSerializer, HistorialSerializer
from rest_framework import generics
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import RegistroUsuarioForm, RegistroPacienteForm
from django.contrib.auth.models import User

class PacienteCreate(generics.ListCreateAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer 

class PacienteDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class HistorialCreate(generics.ListCreateAPIView):
    queryset = HistorialMedico.objects.all()
    serializer_class = HistorialSerializer

class HistorialDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = HistorialMedico.objects.all()
    serializer_class = HistorialSerializer

@login_required
def paciente_dashboard(request):
    # Obtener paciente relacionado al usuario logueado
    paciente = getattr(request.user, 'paciente', None)
    if not paciente:
        return render(request, 'Paciente/error.html', {'mensaje': 'No hay paciente asociado a este usuario.'})

    historial = HistorialMedico.objects.filter(paciente=paciente).order_by('-fecha_consulta')

    contexto = {
        'paciente': paciente,
        'historial': historial
    }
    return render(request, 'Paciente/PacienteDashboard.html', contexto)

def registro(request):
    if request.method == "POST":
        user_form = RegistroUsuarioForm(request.POST)
        paciente_form = RegistroPacienteForm(request.POST)
        if user_form.is_valid() and paciente_form.is_valid():
            # Crear usuario
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Crear paciente vinculado
            paciente = paciente_form.save(commit=False)
            paciente.user = user
            paciente.save()

            # Loguear automáticamente
            login(request, user)
            return redirect('cliente_dashboard')
    else:
        user_form = RegistroUsuarioForm()
        paciente_form = RegistroPacienteForm()

    contexto = {'user_form': user_form, 'paciente_form': paciente_form}
    return render(request, 'registration/registro.html', contexto)