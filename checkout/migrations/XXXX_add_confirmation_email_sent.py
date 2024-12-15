from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='confirmation_email_sent',
            field=models.BooleanField(default=False),
        ),
    ] 