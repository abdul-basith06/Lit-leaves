# Generated by Django 4.2.6 on 2023-10-21 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0006_remove_product_images_alter_productimage_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.product'),
        ),
    ]
