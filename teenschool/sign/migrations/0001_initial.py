# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('startTime', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num', models.CharField(max_length=11)),
                ('name', models.CharField(max_length=50, null=True)),
                ('typ', models.IntegerField()),
                ('signTime', models.DateTimeField()),
                ('signIp', models.IPAddressField()),
                ('project', models.ForeignKey(to='sign.Project')),
            ],
            options={
                'verbose_name': 'Record',
                'verbose_name_plural': 'Records',
            },
            bases=(models.Model,),
        ),
    ]
