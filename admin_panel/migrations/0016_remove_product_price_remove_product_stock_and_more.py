# Generated by Django 4.2.6 on 2023-11-07 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0015_remove_categories_languages_remove_product_languages_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
        migrations.AddField(
            model_name='productlanguagevariation',
            name='price',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='productlanguagevariation',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
