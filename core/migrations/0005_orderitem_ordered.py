# Generated by Django 2.1.1 on 2020-03-20 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200224_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
    ]
