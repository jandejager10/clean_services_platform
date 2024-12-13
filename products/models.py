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


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, 
                               on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )
    sku = models.CharField(max_length=254, null=True, blank=True)
    
    # Change this field to use static files instead of media
    image = models.CharField(
        max_length=254, 
        null=True, 
        blank=True,
        help_text="Image filename from static/images/ directory"
    )

    def __str__(self):
        return self.name

    def get_image_url(self):
        """
        Returns the correct static URL for the image
        """
        if self.image:
            return f'images/{self.image}'
        return 'images/noimage.png'