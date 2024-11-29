from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Creates the default site for the application'

    def handle(self, *args, **kwargs):
        if Site.objects.exists():
            self.stdout.write('Deleting existing sites...')
            Site.objects.all().delete()

        site = Site.objects.create(
            id=1,
            domain='127.0.0.1:8000',
            name='Clean Services Platform'
        )
        self.stdout.write(self.style.SUCCESS(f'Successfully created site: {site.name}')) 