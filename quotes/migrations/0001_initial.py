# Generated by Django 5.0.4 on 2024-04-06 12:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currencies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, max_length=20, null=True, verbose_name='Currency label')),
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
            },
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=125, null=True, verbose_name='Title')),
                ('additional_details', models.CharField(blank=True, max_length=300, null=True, verbose_name='Additional details')),
                ('name', models.CharField(blank=True, max_length=125, null=True, verbose_name='Name')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('quotation_ref', models.IntegerField(blank=True, null=True, verbose_name='Quotation ref')),
                ('quotation_number', models.IntegerField(blank=True, null=True, verbose_name='Quotation number')),
                ('origin', models.CharField(blank=True, max_length=125, null=True, verbose_name='Origin')),
                ('service_type', models.CharField(blank=True, choices=[('DOOR2DOOR', 'Door to Door'), ('Door2Port', 'Door to Port'), ('Port2Door', 'Port to Door'), ('Port2Port', 'Port to Port')], default='DOOR2DOOR', max_length=125, null=True, verbose_name='Service type')),
                ('method', models.CharField(blank=True, max_length=125, null=True, verbose_name='Method')),
                ('volume', models.IntegerField(blank=True, null=True, verbose_name='Volume')),
                ('destination', models.CharField(blank=True, max_length=125, null=True, verbose_name='Destination')),
                ('freight_mode', models.CharField(blank=True, max_length=125, null=True, verbose_name='Freight mode')),
                ('transit_time', models.IntegerField(blank=True, null=True, verbose_name='Transit time')),
                ('weight_up_to', models.CharField(blank=True, max_length=125, null=True, verbose_name='Weight Up to')),
            ],
            options={
                'verbose_name': 'Quote',
                'verbose_name_plural': 'Quotes',
            },
        ),
        migrations.CreateModel(
            name='ServiceExcludes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, max_length=125, null=True, verbose_name='Service name')),
                ('is_checked', models.BooleanField(default=False, verbose_name='')),
                ('quote', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='quote', to='quotes.quote')),
            ],
            options={
                'verbose_name': 'Service item',
                'verbose_name_plural': 'Service items',
            },
        ),
        migrations.CreateModel(
            name='ServiceIncludes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, max_length=125, null=True, verbose_name='Service name')),
                ('is_checked', models.BooleanField(default=False, verbose_name='')),
                ('service', models.CharField(blank=True, choices=[('origin_services', 'Origin Services'), ('international_freight', 'International Freight'), ('destination_services', 'Destination Services'), ('add', 'add')], max_length=25, null=True, verbose_name='Services')),
                ('quote', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='quote', to='quotes.quote')),
            ],
            options={
                'verbose_name': 'Service item',
                'verbose_name_plural': 'Service items',
            },
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=125, null=True, verbose_name='Description')),
                ('supplier', models.CharField(blank=True, max_length=125, null=True, verbose_name='Supplier')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='Quantity')),
                ('buy_price', models.IntegerField(blank=True, null=True, verbose_name='Buy price')),
                ('sale_price', models.IntegerField(blank=True, null=True, verbose_name='Sale price')),
                ('vat', models.BooleanField(default=False, verbose_name='Vat')),
                ('is_required', models.BooleanField(default=False, verbose_name='Is required service')),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quotes.currencies')),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quotes.quote')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
        ),
    ]