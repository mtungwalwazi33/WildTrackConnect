from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('accommodation', 'Safari Accommodation'),
        ('game_drives', 'Game Drives'),
        ('camping', 'Camping Equipment'),
        ('photography', 'Photography Equipment'),
        ('hunting', 'Hunting Equipment'),
        ('drones', 'Monitoring Drones'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True)

    def __str__(self):
        return self.name
