# Generated by Django 4.2.4 on 2024-01-05 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myinvestment', '0005_purchased_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investmentplan',
            name='amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
