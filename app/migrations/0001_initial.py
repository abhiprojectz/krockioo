# Generated by Django 4.2.3 on 2023-07-08 05:57

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
            name='UserBoards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('board_id', models.CharField(max_length=20, unique=True)),
                ('board_name', models.CharField(max_length=300)),
                ('board_image', models.URLField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Boards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slide_id', models.IntegerField(unique=True)),
                ('slide_image', models.URLField(blank=True)),
                ('prompt_content', models.TextField(blank=True)),
                ('board_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.userboards')),
            ],
        ),
    ]
