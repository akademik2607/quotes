# Generated by Django 5.0.4 on 2024-04-18 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0004_quote_total_total_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='sum_buy_filelds',
            field=models.FloatField(blank=True, null=True, verbose_name='Sum buy'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='total_total_sale',
            field=models.FloatField(blank=True, null=True, verbose_name='Total sale'),
        ),
    ]
