# Generated by Django 5.1.6 on 2025-03-01 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_booking_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='bandteam',
            name='booking_fee',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
