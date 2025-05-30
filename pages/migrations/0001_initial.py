# Generated by Django 5.2 on 2025-04-23 11:02

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdviceBaby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advice_baby', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AdviceBad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advice_bad', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AdviceBottel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advice_baby', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AdviceMoon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advice_baby', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AdviceMother',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advice_mather', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baby', models.CharField(max_length=190, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('type', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=200, null=True)),
                ('feedings', models.CharField(max_length=190, null=True)),
                ('sleeping', models.CharField(max_length=190, null=True)),
                ('Diapers', models.CharField(max_length=190, null=True)),
                ('weight', models.FloatField(default=0.0)),
                ('height', models.FloatField(default=0.0)),
                ('photo', models.ImageField(blank=True, default='super.png', null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='GrowthRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField(default=0.0)),
                ('height', models.FloatField(default=0.0)),
                ('datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('child', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='growth_records', to='pages.child')),
            ],
        ),
        migrations.CreateModel(
            name='HowTo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(null=True)),
                ('datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('advice_bad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='howto_bad', to='pages.advicebad')),
                ('advice_bottle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='howto_bottle', to='pages.advicebaby')),
                ('advice_moon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='howto_moon', to='pages.advicemother')),
                ('advice_mother', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='howto_mother', to='pages.advicemother')),
            ],
        ),
        migrations.CreateModel(
            name='Mother',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=190, null=True)),
                ('last_name', models.CharField(max_length=190, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='child',
            name='mother',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pages.mother'),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('content', models.TextField(null=True)),
                ('child', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='pages.child')),
            ],
        ),
    ]
