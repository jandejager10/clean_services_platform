# Generated by Django 5.1.3 on 2024-11-27 16:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FAQCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True)),
                ('order', models.IntegerField(default=0, help_text='Order in which category appears')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'FAQ Category',
                'verbose_name_plural': 'FAQ Categories',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='FAQItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('answer', models.TextField()),
                ('order', models.IntegerField(default=0, help_text='Order in which question appears within category')),
                ('is_active', models.BooleanField(default=True, help_text='Whether this FAQ is visible to users')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faq.faqcategory')),
            ],
            options={
                'verbose_name': 'FAQ Item',
                'verbose_name_plural': 'FAQ Items',
                'ordering': ['category', 'order', 'question'],
                'indexes': [models.Index(fields=['category', 'order'], name='faq_faqitem_categor_913d0b_idx'), models.Index(fields=['is_active'], name='faq_faqitem_is_acti_e09e0d_idx')],
            },
        ),
    ]
