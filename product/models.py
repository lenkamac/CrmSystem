from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    net_price = models.DecimalField(max_digits=10, decimal_places=2)
    sold_quantity = models.IntegerField(default=0)  # Track total sold
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name