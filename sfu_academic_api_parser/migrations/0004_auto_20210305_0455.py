# Generated by Django 3.1.6 on 2021-03-05 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sfu_academic_api_parser', '0003_auto_20210305_0445'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='description',
            field=models.CharField(default='This is an example description', max_length=1000),
        ),
        migrations.AddField(
            model_name='course',
            name='number_str',
            field=models.CharField(default='TEST 123', max_length=10),
        ),
    ]