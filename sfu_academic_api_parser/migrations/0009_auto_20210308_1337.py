# Generated by Django 3.1.6 on 2021-03-08 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sfu_academic_api_parser', '0008_auto_20210308_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='units',
            field=models.CharField(default='0', max_length=10),
        ),
    ]