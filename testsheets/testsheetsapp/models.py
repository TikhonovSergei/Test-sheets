from django.db import models

class Orders(models.Model):
    number = models.CharField(max_length=100, null=True, blank=True)
    number_order = models.CharField(max_length=100, null=True, blank=True)
    price_dolars = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    price_rubles = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    data_deliveries = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.number_order}"

