# core/admin.py

from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Solicitud, Comentario, MaterialType, PuntoLimpio, Recomendacion


# -----------------------------------------------------------------------------------
# 1) Formulario personalizado para Solicitud:
#    Limita el dropdown de "operario" a usuarios que pertenezcan al grupo 'operarios'.
# -----------------------------------------------------------------------------------
class SolicitudAdminForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegúrate de que el nombre del grupo coincida exactamente con el que existe en Admin → Grupos
        if 'operario' in self.fields:
            self.fields['operario'].queryset = User.objects.filter(
                groups__name='operarios'
            ).order_by('username')


# -----------------------------------------------------------------------------------
# 2) Inline de Comentario:
#    - Model: Comentario
#    - Mostrar: campo 'texto' editable, y 'autor'/'fecha' como read-only.
# -----------------------------------------------------------------------------------
class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 1
    fields = ('texto', 'autor', 'fecha')
    readonly_fields = ('autor', 'fecha')


# -----------------------------------------------------------------------------------
# 3) SolicitudAdmin: registra el inline, el filtrado y permisos
#    - NO hay get_fields en absoluto.
# -----------------------------------------------------------------------------------
@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    form = SolicitudAdminForm
    inlines = [ComentarioInline]

    # Columnas que se muestran en la lista de solicitudes
    list_display = ('ciudadano', 'material', 'cantidad', 'estado', 'operario')
    list_filter = ('estado', 'operario')
    search_fields = ('ciudadano__username', 'material__nombre')
    raw_id_fields = ('ciudadano', 'material')

    # --------------------------------------------------------------------------------
    # 3.1) get_queryset: qué solicitudes ve cada usuario en la lista
    #    - Superuser: ve todo
    #    - Operario (sin comprobar grupo): solo las solicitudes donde operario=request.user
    #    - Cualquier otro usuario: no ve nada (QuerySet vacío)
    # --------------------------------------------------------------------------------
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Liberamos la dependencia de grupo: filtramos directamente por el campo operario
        return qs.filter(operario=request.user)

    # --------------------------------------------------------------------------------
    # 3.2) get_readonly_fields: 
    #    - Superuser: no bloquea nada
    #    - Operario editando una solicitud existente (obj != None):
    #        bloquea todos los campos salvo 'estado' (y el inline de Comentarios)
    # --------------------------------------------------------------------------------
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        # Si estamos editando (obj != None), y el usuario es ese operario
        if obj is not None and obj.operario == request.user:
            # Bloqueamos todo excepto 'estado'
            return [
                'ciudadano',
                'material',
                'cantidad',
                'fecha_estimada',
                'operario',
                'fecha_completada',
            ]
        return []

    # --------------------------------------------------------------------------------
    # 3.3) has_view_permission y has_change_permission:
    #    - Superuser: True siempre
    #    - Vista de lista (obj=None): True, pero el queryset ya está filtrado
    #    - Vista de detalle (obj != None): True solo si obj.operario == request.user
    # --------------------------------------------------------------------------------
    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        return obj.operario == request.user

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        return obj.operario == request.user

    # --------------------------------------------------------------------------------
    # 3.4) has_delete_permission y has_add_permission:
    #    - Solo superuser puede eliminar o agregar Solicitudes desde Admin
    # --------------------------------------------------------------------------------
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    # --------------------------------------------------------------------------------
    # 3.5) formfield_for_foreignkey:
    #    - Evita que un operario reasigne la solicitud a otro
    # --------------------------------------------------------------------------------
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if (
            db_field.name == "operario"
            and not request.user.is_superuser
            and request.user == getattr(request.resolver_match.func.view_class, 'model', None)
        ):
            # Forzamos que el dropdown quede vacío para operarios
            kwargs["queryset"] = Solicitud.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # --------------------------------------------------------------------------------
    # 3.6) save_related:
    #    - Antes de guardar el inline de Comentarios, asignamos autor=request.user y fecha=ahora
    # --------------------------------------------------------------------------------
    def save_related(self, request, form, formsets, change):
        for formset in formsets:
            for subform in formset.forms:
                if isinstance(subform.instance, Comentario) and subform.instance.pk is None:
                    subform.instance.autor = request.user
                    subform.instance.fecha = timezone.now()
        super().save_related(request, form, formsets, change)


# -----------------------------------------------------------------------------------
# 4) Registramos el resto de modelos sin customizaciones:
# -----------------------------------------------------------------------------------
admin.site.register(MaterialType)
admin.site.register(PuntoLimpio)
admin.site.register(Recomendacion)

# ¡OJO!: NO registramos Comentario por separado. El inline ya lo presenta en SolicitudAdmin.
