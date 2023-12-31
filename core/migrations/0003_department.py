# Generated by Django 4.2.7 on 2023-11-13 23:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_costcenter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=100)),
                ('integration_code', models.CharField(max_length=100)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='core.company')),
                ('cost_center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='core.costcenter')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
