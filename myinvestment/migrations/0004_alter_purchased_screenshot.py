# Generated by Django 4.2.4 on 2024-01-04 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myinvestment', '0003_purchased'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchased',
            name='screenshot',
            field=models.FileField(blank=True, null=True, upload_to='files'),
        ),
    ]
