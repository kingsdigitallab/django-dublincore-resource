# Generated by Django 3.0.8 on 2020-07-27 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dublincore_resource', '0004_auto_20191211_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dublincoreagent',
            name='identifier',
            field=models.URLField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='dublincoreresource',
            name='title',
            field=models.CharField(help_text='A name given to the resource.', max_length=500),
        ),
    ]