# Generated by Django 5.2 on 2025-05-05 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_task_child'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='datetime',
        ),
    ]
