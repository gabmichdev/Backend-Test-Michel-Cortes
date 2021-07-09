# Generated by Django 3.0.8 on 2021-07-08 01:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20210708_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='meal_time',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Desayuno'), (2, 'Comida'), (3, 'Cena'), (4, 'After')], default=2, unique_for_date='preparation_date'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='preparation_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
