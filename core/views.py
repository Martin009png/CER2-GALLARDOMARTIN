from django.shortcuts import redirect, render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import logout  

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