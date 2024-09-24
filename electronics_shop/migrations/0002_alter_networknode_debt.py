# Generated by Django 5.1.1 on 2024-09-16 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electronics_shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networknode',
            name='debt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Задолженность перед поставщиком'),
        ),
    ]
