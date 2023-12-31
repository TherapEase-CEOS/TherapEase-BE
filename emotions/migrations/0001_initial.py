# Generated by Django 3.2.16 on 2023-07-17 15:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Emotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_emotion', models.CharField(choices=[('sad', 'Sad'), ('scared', 'Scared'), ('joyful', 'Joyful'), ('powerful', 'Powerful'), ('peaceful', 'Peaceful'), ('mad', 'Mad')], max_length=10)),
                ('sub_emotion', models.CharField(max_length=50)),
                ('feeling', models.CharField(choices=[('-1', 'Negative'), ('0', 'Neutral'), ('1', 'Positive')], default='-1', max_length=2)),
                ('intensity', models.IntegerField()),
                ('details1', models.TextField(blank=True, null=True)),
                ('details2', models.TextField(blank=True, null=True)),
                ('details3', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emotions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
