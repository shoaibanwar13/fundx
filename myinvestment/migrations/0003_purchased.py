# Generated by Django 4.2.4 on 2024-01-04 15:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myinvestment', '0002_investmentplan'),
    ]

    operations = [
        migrations.CreateModel(
            name='purchased',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(max_length=100)),
                ('pay_method', models.CharField(max_length=30)),
                ('trans_id', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved')], default='Pending', max_length=20)),
                ('screenshot', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchase', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Purchased',
                'ordering': ('-created_at',),
            },
        ),
    ]