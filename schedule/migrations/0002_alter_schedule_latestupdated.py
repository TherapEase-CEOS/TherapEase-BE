# Generated by Django 3.2.16 on 2023-07-29 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='latestUpdated',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]