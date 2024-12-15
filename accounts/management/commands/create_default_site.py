from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Creates or updates the default site'

    def handle(self, *args, **kwargs):
        # Get or create site with ID 1
        site, created = Site.objects.get_or_create(
            id=1,
            defaults={
                'domain': 'codeinstproj4-resub-79196432a6ce.herokuapp.com',
                'name': 'Clean Services Platform'
            }
        )

        if not created:
            site.domain = 'codeinstproj4-resub-79196432a6ce.herokuapp.com'
            site.name = 'Clean Services Platform'
            site.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully {"created" if created else "updated"} site: {site.domain}'
            )
        ) 