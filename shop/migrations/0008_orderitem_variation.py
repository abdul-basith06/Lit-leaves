# Generated by Django 4.2.6 on 2023-11-08 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0017_remove_productlanguagevariation_price_product_price'),
        ('shop', '0007_order_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='variation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_panel.productlanguagevariation'),
        ),
    ]
