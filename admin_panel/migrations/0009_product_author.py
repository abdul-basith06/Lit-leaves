# Generated by Django 4.2.6 on 2023-10-24 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0008_alter_productimage_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='author',
            field=models.CharField(default='basi', max_length=100),
        ),
    ]
