from django.db import models
from django.contrib.auth.models import User

class Electrodomestico(models.Model):
    TIPO_CHOICES = [
        ('convencional', 'Convencional'),
        ('eficiente', 'Eficiente'),
    ]
    CATEGORIAS = [
        ('cocina', 'Cocina'),
        ('limpieza', 'Limpieza'),
        ('refrigeracion', 'Refrigeración'),
        ('climatizacion','Climatización'),
        ('cuidado_personal', 'Cuidado personal'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    potencia_w = models.FloatField()
    horas_uso_diario = models.FloatField()
    
    def consumo_mensual(self):
        return (self.potencia * self.horas_uso * 30) / 1000  

    def consumo_anual(self):
        return self.consumo_mensual() * 12

    def costo_mensual(self, tarifa):
        return self.consumo_mensual() * tarifa

    def costo_anual(self, tarifa):
        return self.consumo_anual() * tarifa

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

class TarifaEnergia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    valor_kwh = models.FloatField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

class CalculoConsumo(models.Model):
    electrodomestico = models.ForeignKey(Electrodomestico, on_delete=models.CASCADE)
    tarifa = models.ForeignKey(TarifaEnergia, on_delete=models.CASCADE)
    consumo_mensual_kwh = models.FloatField()
    consumo_anual_kwh = models.FloatField()
    costo_mensual = models.FloatField()
    costo_anual = models.FloatField()
    huella_carbono_mensual = models.FloatField()
    huella_carbono_anual = models.FloatField()
    fecha_calculo = models.DateTimeField(auto_now_add=True)

