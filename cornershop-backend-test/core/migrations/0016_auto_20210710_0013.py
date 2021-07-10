# Generated by Django 3.0.8 on 2021-07-10 00:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20210710_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='added_by_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='menuselection',
            name='menu',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.Menu'),
            preserve_default=False,
        ),
    ]