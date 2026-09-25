from django.contrib import admin
from .models import Cliente, Cuenta, Transaccion

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email', 'telefono', 'fecha_registro', 'usuario')
    search_fields = ('nombre', 'email')

@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ('id','numero_cuenta', 'cliente', 'tipo_cuenta', 'saldo')
    list_filter = ('tipo_cuenta',)
    search_fields = ('numero_cuenta', 'cliente__nombre')
    # Permite gestionar fácilmente los contactos autorizados con una interfaz cómoda:
    filter_horizontal = ('contactos_autorizados',)
    
@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    # Reemplazamos 'monto' por nuestro método personalizado 'monto_formateado'
    list_display = ('id', 'tipo', 'cuenta_origen', 'cuenta_destino', 'monto_formateado', 'fecha')
    list_filter = ('tipo','fecha')
    search_fields = ('cuenta_origen__numero_cuenta', 'cuenta_destino__numero_cuenta')

    # Función personalizada para dar formato de moneda
    def monto_formateado(self, obj):
        if obj.monto is not None:
            # Opción 1: Formato estándar ($1,000,000.00)
            return f"${obj.monto:,.2f}"
            
            # Opción 2: Formato chileno sin decimales ($1.000.000)
            # return f"${int(obj.monto):,}".replace(",", ".")
        return "$0.00"

    




