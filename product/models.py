from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2,  default=0 )
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

CHOICES = [(i, i) for i in range(1, 6)]

class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    stars = models.IntegerField(choices=CHOICES, default=3)

    def __str__(self):
        return f'{self.stars}'

