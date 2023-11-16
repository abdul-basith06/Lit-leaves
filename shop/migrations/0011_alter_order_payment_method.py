# Generated by Django 4.2.6 on 2023-11-16 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_alter_orderitem_delivery_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('COD', 'Cash on Delivery'), ('RAZ', 'Paid With Razorpay')], max_length=20, null=True),
        ),
    ]
