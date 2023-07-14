# Generated by Django 3.2.16 on 2023-07-13 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sunday', models.JSONField(default=list)),
                ('monday', models.JSONField(default=list)),
                ('tuesday', models.JSONField(default=list)),
                ('wednesday', models.JSONField(default=list)),
                ('thursday', models.JSONField(default=list)),
                ('friday', models.JSONField(default=list)),
                ('saturday', models.JSONField(default=list)),
                ('latestUpdated', models.DateField()),
            ],
        ),
    ]