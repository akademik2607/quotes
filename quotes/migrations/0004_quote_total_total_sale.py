# Generated by Django 5.0.4 on 2024-04-18 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0003_remove_quote_destination_quote_destination_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='total_total_sale',
            field=models.IntegerField(blank=True, null=True, verbose_name='Total sale time'),
        ),
    ]
