from django.db import migrations

def set_default_status(apps, schema_editor):
    Order = apps.get_model('checkout', 'Order')
    Order.objects.filter(status__isnull=True).update(status='processing')

class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_default_status),
    ] 