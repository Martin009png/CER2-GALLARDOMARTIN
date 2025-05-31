from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from .models import Comentario, MaterialType, PuntoLimpio, Recomendacion, Solicitud

class SolicitudAdminForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo ajustamos queryset si el campo 'operario' existe en el formulario
        if 'operario' in self.fields:
            self.fields['operario'].queryset = User.objects.filter(groups__name='operarios').order_by('username')
class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 0
    readonly_fields = ('autor', 'fecha')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.autor = request.user
        super().save_model(request, obj, form, change)

class SolicitudAdmin(admin.ModelAdmin):
    inlines = [ComentarioInline]
    form = SolicitudAdminForm
    list_display = ('ciudadano', 'material', 'cantidad', 'estado', 'operario')
    list_filter = ('estado', 'operario')
    search_fields = ('ciudadano__username', 'material__nombre')
    raw_id_fields = ('ciudadano', 'material')
    inlines = [ComentarioInline]

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='operarios').exists():
            return ('operario',)
        return ()

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if request.user.groups.filter(name='operarios').exists():
            fields = [f for f in fields if f != 'operario']
        return fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_staff:
            return qs
        if request.user.groups.filter(name='operarios').exists():
            return qs.filter(operario=request.user)
        return qs.none()

admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(MaterialType)
admin.site.register(PuntoLimpio)
admin.site.register(Recomendacion)
admin.site.register(Comentario)
