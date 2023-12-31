# Generated by Django 4.2.6 on 2023-11-20 05:56

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0012_alter_order_payment_method'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('valid_from', models.DateTimeField(default=django.utils.timezone.now)),
                ('valid_till', models.DateTimeField()),
                ('discount_amount', models.PositiveIntegerField()),
                ('min_purchase_amount', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('used_by', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
