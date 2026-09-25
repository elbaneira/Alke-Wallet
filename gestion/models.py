# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    # Enlace uno a uno con el usuario de Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.email})"

class Cuenta(models.Model):
    TIPO_CUENTA_CHOICES = [
        ('AHORRO', 'Cuenta de Ahorro'),
        ('CORRIENTE', 'Cuenta Corriente'),
        ('VIRTUAL', 'Billetera Virtual'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='cuentas')
    numero_cuenta = models.CharField(max_length=20, unique=True)
    tipo_cuenta = models.CharField(max_length=10, choices=TIPO_CUENTA_CHOICES, default='VIRTUAL')
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    creada_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cuenta {self.numero_cuenta} - {self.cliente.nombre} (${self.saldo})"

class Transaccion(models.Model):
    TIPO_TRANSACCION_CHOICES = [
        ('DEPOSITO', 'Depósito'),
        ('RETIRO', 'Retiro'),
        ('TRANSFERENCIA', 'Transferencia'),
    ]

    cuenta_origen = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='transacciones_salida')
    cuenta_destino = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='transacciones_entrada', null=True, blank=True)
    tipo = models.CharField(max_length=15, choices=TIPO_TRANSACCION_CHOICES)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} de ${self.monto} - Cuenta {self.cuenta_origen.numero_cuenta}"
