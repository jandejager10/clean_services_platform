from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name
        
    def get_friendly_name(self):
        return self.friendly_name


class Service(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, 
                               on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=1,
                               null=True, blank=True,
                               validators=[
                                   MinValueValidator(0),
                                   MaxValueValidator(5)
                               ])
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    is_recurring = models.BooleanField(default=False)
    frequency = models.CharField(max_length=50, null=True, blank=True,
                               choices=[
                                   ('weekly', 'Weekly'),
                                   ('bi-weekly', 'Bi-Weekly'),
                                   ('monthly', 'Monthly'),
                               ])
    
    def __str__(self):
        return self.name 