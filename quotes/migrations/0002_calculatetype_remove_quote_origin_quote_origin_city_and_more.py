# Generated by Django 5.0.4 on 2024-04-17 22:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalculateType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, max_length=20, null=True, verbose_name='Calculate type label')),
            ],
            options={
                'verbose_name': 'Calculate type',
                'verbose_name_plural': 'Calculate types',
            },
        ),
        migrations.RemoveField(
            model_name='quote',
            name='origin',
        ),
        migrations.AddField(
            model_name='quote',
            name='origin_city',
            field=models.CharField(blank=True, max_length=125, null=True, verbose_name='Origin City'),
        ),
        migrations.AddField(
            model_name='quote',
            name='origin_country',
            field=models.CharField(blank=True, max_length=125, null=True, verbose_name='Origin Country'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='method',
            field=models.CharField(blank=True, choices=[('Sea', 'Sea'), ('Air', 'Air')], max_length=125, null=True, verbose_name='Method'),
        ),
        migrations.AddField(
            model_name='services',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quotes.calculatetype'),
        ),
    ]