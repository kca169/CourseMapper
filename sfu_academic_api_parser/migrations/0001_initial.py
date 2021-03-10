# Generated by Django 3.1.6 on 2021-03-10 04:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='This is an example title', max_length=50)),
                ('number_str', models.CharField(default='TEST 123', max_length=12)),
                ('description', models.CharField(default='This is an example description', max_length=1000)),
                ('code', models.CharField(default='TEST', max_length=5)),
                ('number', models.IntegerField(default=123)),
                ('year', models.IntegerField(default=2021)),
                ('semester', models.CharField(default='New example', max_length=15)),
                ('units', models.IntegerField()),
                ('grade', models.CharField(default='NI', max_length=3)),
                ('prerequisites', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sfu_academic_api_parser.course')),
            ],
        ),
    ]
