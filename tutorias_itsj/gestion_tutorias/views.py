from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroForm

def landing(request):
    return render(request, 'gestion_tutorias/landing.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistroForm()
    return render(request, 'gestion_tutorias/registro.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .models import Tutoria, Mensaje

@login_required
def dashboard(request):
    context = {}
    
    if request.user.tipo_usuario == 'Tutor':
        tutorias = Tutoria.objects.filter(tutor=request.user).order_by('-fecha', '-hora')[:5]
        mensajes = Mensaje.objects.filter(destinatario=request.user).order_by('-fecha_envio')[:5]
        context.update({
            'tutorias': tutorias,
            'mensajes': mensajes,
            'es_tutor': True
        })
    elif request.user.tipo_usuario == 'Estudiante':
        tutorias = Tutoria.objects.filter(estudiante=request.user).order_by('-fecha', '-hora')[:5]
        mensajes = Mensaje.objects.filter(destinatario=request.user).order_by('-fecha_envio')[:5]
        context.update({
            'tutorias': tutorias,
            'mensajes': mensajes,
            'es_estudiante': True
        })
    else:  # Administrador
        tutorias = Tutoria.objects.all().order_by('-fecha', '-hora')[:10]
        context.update({
            'tutorias': tutorias,
            'es_admin': True
        })
    
    return render(request, 'gestion_tutorias/dashboard.html', context)

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Tutoria
from .forms import TutoriaForm

class TutoriaListView(ListView):
    model = Tutoria
    template_name = 'gestion_tutorias/tutoria_list.html'
    context_object_name = 'tutorias'
    
    def get_queryset(self):
        if self.request.user.tipo_usuario == 'Tutor':
            return Tutoria.objects.filter(tutor=self.request.user)
        elif self.request.user.tipo_usuario == 'Estudiante':
            return Tutoria.objects.filter(estudiante=self.request.user)
        return Tutoria.objects.all()

class TutoriaCreateView(CreateView):
    model = Tutoria
    form_class = TutoriaForm
    template_name = 'gestion_tutorias/tutoria_form.html'
    success_url = reverse_lazy('tutoria-list')
    
    def form_valid(self, form):
        if self.request.user.tipo_usuario == 'Estudiante':
            form.instance.estudiante = self.request.user
        elif self.request.user.tipo_usuario == 'Tutor':
            form.instance.tutor = self.request.user
        return super().form_valid(form)

class TutoriaUpdateView(UpdateView):
    model = Tutoria
    form_class = TutoriaForm
    template_name = 'gestion_tutorias/tutoria_form.html'
    success_url = reverse_lazy('tutoria-list')

class TutoriaDeleteView(DeleteView):
    model = Tutoria
    template_name = 'gestion_tutorias/tutoria_confirm_delete.html'
    success_url = reverse_lazy('tutoria-list')