from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    net_price = models.DecimalField(max_digits=10, decimal_places=2)
    sold_quantity = models.IntegerField(default=0)  # Track total sold
    description = models.TextField(blank=True, null=True)

    def get_total_price(self):
        """Calculate total price based on net price and sold quantity"""
        return self.net_price * self.sold_quantity

    def __str__(self):
        return self.name