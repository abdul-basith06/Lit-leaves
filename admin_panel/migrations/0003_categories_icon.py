# Generated by Django 4.2.6 on 2023-10-20 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0002_categories_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='category_icons/'),
        ),
    ]
