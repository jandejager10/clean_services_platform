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
    
    def get_detail_image(self):
        """Returns the appropriate detail image for this service"""
        image_mapping = {
            'home_cleaning': 'images/house-cleaning-detail.jpg',
            'office_cleaning': 'images/office-maintenance.jpg',
            'deep_cleaning': 'images/sanitization-service.jpg',
            'move_in_move_out_cleaning': 'images/property-turnover.jpg',
            'post_renovation_cleaning': 'images/builders-clean.jpg',
            'recurring_home_cleaning': 'images/scheduled-maintenance.jpg',
            'recurring_office_cleaning': 'images/recurring-office-clean.jpg',
        }
        
        # Get service type from category and clean it
        service_type = self.category.name.lower().strip()
        print(f"Service type: {service_type}")  # Debug print
        print(f"Available mappings: {list(image_mapping.keys())}")  # Debug print
        
        # Get mapped image or default
        image = image_mapping.get(service_type, 'images/noimage.png')
        print(f"Mapped image: {image}")  # Debug print
        
        return image