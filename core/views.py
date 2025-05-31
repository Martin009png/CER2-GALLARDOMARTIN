from django.shortcuts import redirect, render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import logout  
from .models import PuntoLimpio, Recomendacion, Solicitud,MaterialType
from django import forms
from django.db.models import Count, Avg, F, ExpressionWrapper, DurationField
from django.db.models.functions import TruncMonth




# Create your views here.
def home(request):
    # Si nunca habíamos visitado la home en esta sesión...
    if not request.session.get('home_visited', False):
        # Marcamos que ya la visitamos
        request.session['home_visited'] = True
        # Y si venimos logueados, forzamos logout para mostrar cliente anónimo
        if request.user.is_authenticated:
            logout(request)
            return redirect('home')

    # En cualquier otra visita, respetamos el login y mostramos nombre si existe
    return render(request, 'core/home.html')

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def materiales_publicos(request):
    materiales = MaterialType.objects.all()
    return render(request, 'core/materiales.html', {'materiales': materiales})

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['material', 'cantidad', 'fecha_estimada']
        widgets = {
            'fecha_estimada': forms.DateInput(attrs={'type': 'date'})
        }

@login_required
def nueva_solicitud(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.ciudadano = request.user
            solicitud.save()
            return redirect('mis_solicitudes')
    else:
        form = SolicitudForm()
    return render(request, 'core/nueva_solicitud.html', {'form': form})

def mis_solicitudes(request):
    solicitudes = Solicitud.objects.filter(ciudadano=request.user).order_by('-created_at')
    return render(request, 'core/mis_solicitudes.html', {'solicitudes': solicitudes})

def puntos_limpios(request):
    puntos = PuntoLimpio.objects.all()
    return render(request, 'core/puntos_limpios.html', {'puntos': puntos})

def recomendaciones(request):
    consejos = Recomendacion.objects.all()
    return render(request, 'core/recomendaciones.html', {'consejos': consejos})

def metricas_reciclaje(request):
    # Cantidad de solicitudes por mes
    solicitudes_por_mes = (
        Solicitud.objects
        .annotate(mes=TruncMonth('created_at'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )

    # Tipo de materiales más reciclados
    solicitudes_por_material = (
        Solicitud.objects
        .values('material__nombre')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # Tiempo promedio de retiro (solo solicitudes completadas)
    tiempo_promedio = (
        Solicitud.objects
        .filter(fecha_completada__isnull=False)
        .annotate(
            duracion=ExpressionWrapper(
                F('fecha_completada') - F('created_at'),
                output_field=DurationField()
            )
        )
        .aggregate(promedio=Avg('duracion'))
    )['promedio']

    context = {
        'solicitudes_por_mes': solicitudes_por_mes,
        'solicitudes_por_material': solicitudes_por_material,
        'tiempo_promedio': tiempo_promedio,
    }

    return render(request, 'core/metricas.html', context)