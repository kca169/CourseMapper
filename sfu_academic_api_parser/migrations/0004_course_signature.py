# Generated by Django 3.1.6 on 2021-03-10 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sfu_academic_api_parser', '0003_course_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='signature',
            field=models.CharField(default='Change this.', max_length=1500, unique=True),
        ),
    ]