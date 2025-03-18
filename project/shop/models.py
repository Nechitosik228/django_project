from django.db import models


class Seller(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

class Product(models.Model):
    class Category(models.TextChoices):
        FD = "FD", "Food"
        TH = "TH", "Tech"
        JW = "JW", "Jewelery"
        TR = "TR", "Transport"

    name = models.CharField(max_length=100)
    entity = models.IntegerField()
    price = models.DecimalField(max_digits=7,decimal_places=2)
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name='posts'
    )