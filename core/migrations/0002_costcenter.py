# Generated by Django 4.2.7 on 2023-11-13 23:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CostCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('code', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=100)),
                ('cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cost_centers', to='core.company')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
