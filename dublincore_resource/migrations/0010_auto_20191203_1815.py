# Generated by Django 2.2.7 on 2019-12-03 18:15

import controlled_vocabulary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('controlled_vocabulary', '0004_controlledvocabulary_concept'),
        ('dublincore_resource', '0009_auto_20191203_0254'),
    ]

    operations = [
        migrations.CreateModel(
            name='DublinCoreRights',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shorthand', models.CharField(blank=True, default='', max_length=50)),
                ('statement', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='dublincoreresource',
            name='date',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AddField(
            model_name='dublincoreresource',
            name='format',
            field=controlled_vocabulary.models.ControlledTermField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='controlled_vocabulary.ControlledTerm'),
        ),
        migrations.AddField(
            model_name='dublincoreresource',
            name='spatial',
            field=controlled_vocabulary.models.ControlledTermField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='controlled_vocabulary.ControlledTerm'),
        ),
        migrations.AddField(
            model_name='dublincoreresource',
            name='subject',
            field=controlled_vocabulary.models.ControlledTermField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='controlled_vocabulary.ControlledTerm'),
        ),
        migrations.AddField(
            model_name='dublincoreresource',
            name='temporal',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='dublincoreresource',
            name='language',
            field=controlled_vocabulary.models.ControlledTermField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='controlled_vocabulary.ControlledTerm'),
        ),
        migrations.AlterField(
            model_name='dublincoreresource',
            name='title',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='dublincoreresource',
            name='type',
            field=controlled_vocabulary.models.ControlledTermField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='controlled_vocabulary.ControlledTerm'),
        ),
        migrations.AddField(
            model_name='dublincoreresource',
            name='rights',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resources', to='dublincore_resource.DublinCoreRights'),
        ),
    ]
