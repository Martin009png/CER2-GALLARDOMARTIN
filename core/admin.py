from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Solicitud, Comentario, MaterialType, PuntoLimpio, Recomendacion


class SolicitudAdminForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo usuarios del grupo "operarios" aparecen en el selector
        if 'operario' in self.fields:
            self.fields['operario'].queryset = User.objects.filter(
                groups__name='operarios'
            ).order_by('username')


class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 1
    fields = ('texto', 'autor', 'fecha')
    readonly_fields = ('autor', 'fecha')  # Autor y fecha se asignan automáticamente


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    form = SolicitudAdminForm
    inlines = [ComentarioInline]

    list_display = ('ciudadano', 'material', 'cantidad', 'estado', 'operario')
    list_filter = ('estado', 'operario')
    search_fields = ('ciudadano__username', 'material__nombre')
    raw_id_fields = ('ciudadano', 'material')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Superusuario ve todo; cada operario solo sus solicitudes
        return qs if request.user.is_superuser else qs.filter(operario=request.user)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        # Si el operario está editando su propia solicitud, solo puede cambiar el estado
        if obj and obj.operario == request.user:
            return ['ciudadano', 'material', 'cantidad', 'fecha_estimada', 'operario', 'fecha_completada']
        return []

    def has_view_permission(self, request, obj=None):
        # Superusuario o lista permitida; detalle solo si es su propia solicitud
        return True if (request.user.is_superuser or obj is None) else (obj.operario == request.user)

    def has_change_permission(self, request, obj=None):
        # Mismas reglas que visualización
        return True if (request.user.is_superuser or obj is None) else (obj.operario == request.user)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Solo superusuario

    def has_add_permission(self, request):
        return request.user.is_superuser  # Solo superusuario

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Evita que el operario reasigne la solicitud a otro
        if (
            db_field.name == "operario"
            and not request.user.is_superuser
            and request.user == getattr(request.resolver_match.func.view_class, 'model', None)
        ):
            kwargs["queryset"] = Solicitud.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_related(self, request, form, formsets, change):
        # Antes de guardar comentarios, asigna autor y fecha
        for formset in formsets:
            for subform in formset.forms:
                if isinstance(subform.instance, Comentario) and not subform.instance.pk:
                    subform.instance.autor = request.user
                    subform.instance.fecha = timezone.now()
        super().save_related(request, form, formsets, change)


# Registra modelos adicionales sin personalizar
admin.site.register(MaterialType)
admin.site.register(PuntoLimpio)
admin.site.register(Recomendacion)
