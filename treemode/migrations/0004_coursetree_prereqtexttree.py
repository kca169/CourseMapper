# Generated by Django 3.1.6 on 2021-03-27 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treemode', '0003_merge_20210319_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursetree',
            name='prereqtexttree',
            field=models.CharField(default=['empty', 'text', 'tree'], max_length=1000),
        ),
    ]
