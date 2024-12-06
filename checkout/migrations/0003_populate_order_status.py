from django.db import migrations


def set_default_status(apps, schema_editor):
    Order = apps.get_model('checkout', 'Order')
    Order.objects.exclude(
        status__in=['pending', 'processing', 'cancellation_requested', 
                    'completed', 'cancelled']
    ).update(status='processing')


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_add_order_status'),
    ]

    operations = [
        migrations.RunPython(set_default_status, reverse_code=migrations.RunPython.noop),
    ] 