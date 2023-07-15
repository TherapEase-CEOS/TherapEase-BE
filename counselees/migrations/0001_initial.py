# Generated by Django 3.2.16 on 2023-07-15 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Counselee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('accountId', models.CharField(max_length=255)),
                ('start', models.DateTimeField()),
                ('progress', models.BooleanField()),
                ('counselingDate', models.CharField(max_length=255)),
                ('goal', models.CharField(default='상담 목표를 입력해주세요!', max_length=255, null=True)),
            ],
        ),
    ]
