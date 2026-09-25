from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Dashboard & Transacciones
    path('login/', auth_views.LoginView.as_view(template_name='gestion/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('transaccion/nueva/', views.crear_transaccion, name='crear_transaccion'),
    
    # CRUD Clientes
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/nuevo/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),

    # CRUD Cuentas
    path('cuentas/nueva/', views.crear_cuenta, name='crear_cuenta'),
    path('cuentas/eliminar/<int:id>/', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('cuenta/<int:id>/', views.detalle_cuenta, name='detalle_cuenta'),
]

