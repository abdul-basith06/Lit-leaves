# Generated by Django 4.2.6 on 2023-11-05 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_order_payment_method_order_shipping_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_notes',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
