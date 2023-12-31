# Generated by Django 4.2.6 on 2023-11-17 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_alter_order_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('COD', 'Cash on Delivery'), ('RAZ', 'Paid With Razorpay'), ('WAL', 'Paid With Wallet')], max_length=20, null=True),
        ),
    ]
