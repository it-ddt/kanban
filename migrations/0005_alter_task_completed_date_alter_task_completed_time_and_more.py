# Generated by Django 4.1.3 on 2023-05-06 11:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanban', '0004_alter_task_deadline_date_alter_task_deadline_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completed_date',
            field=models.DateField(default=datetime.date(2023, 5, 6)),
        ),
        migrations.AlterField(
            model_name='task',
            name='completed_time',
            field=models.TimeField(default=datetime.date(2023, 5, 6)),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline_time',
            field=models.TimeField(default=datetime.time(11, 18, 11, 391966)),
        ),
    ]
