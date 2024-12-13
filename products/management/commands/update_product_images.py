from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Updates product image paths to use static files'

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        updated = 0

        for product in products:
            if product.image:
                # Extract filename from media URL or path
                filename = product.image.name.split('/')[-1]
                product.image = filename
                product.save()
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {updated} product image paths'
            )
        ) 