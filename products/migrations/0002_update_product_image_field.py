# Generated by Django 5.1.3
from django.db import migrations, models
from django.core.validators import MinValueValidator, MaxValueValidator

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),  # This should be the actual initial migration
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image_url',
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.CharField(
                blank=True,
                help_text='Image filename from static/images/ directory',
                max_length=254,
                null=True
            ),
        ),
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=3,
                null=True,
                validators=[
                    MinValueValidator(0),
                    MaxValueValidator(5)
                ]
            ),
        ),
    ] 