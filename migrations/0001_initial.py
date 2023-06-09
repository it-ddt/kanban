# Generated by Django 4.2.1 on 2023-06-04 19:21

import datetime
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
            name='Kanban',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Доски',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='название')),
                ('description', models.TextField(verbose_name='описание')),
                ('status', models.CharField(default='new', max_length=100, verbose_name='статус')),
                ('created_date', models.DateField(default=datetime.date(2023, 6, 4))),
                ('created_time', models.TimeField(default=datetime.time(19, 21, 26, 620810))),
                ('assigned_date', models.DateField(blank=True, null=True)),
                ('assigned_time', models.TimeField(blank=True, null=True)),
                ('deadline_date', models.DateField(blank=True, null=True, verbose_name='дедлайн дата')),
                ('deadline_time', models.TimeField(blank=True, null=True, verbose_name='дедлайн время')),
                ('completed_date', models.DateField(blank=True, null=True)),
                ('completed_time', models.TimeField(blank=True, null=True)),
                ('executor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='исполнитель')),
                ('kanban', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='kanban.kanban')),
            ],
            options={
                'verbose_name_plural': 'Задачи',
            },
        ),
    ]
