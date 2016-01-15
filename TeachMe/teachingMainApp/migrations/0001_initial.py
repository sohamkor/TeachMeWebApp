# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Learner',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('pointsEarned', models.IntegerField(default=0)),
                ('versionOfSite', models.CharField(default='1.0.0', max_length=40)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='coach',
            name='theUserWhoIsTheCoach',
            field=models.ForeignKey(to='teachingMainApp.Learner', related_name='userWhoIsTheCoach'),
        ),
        migrations.AddField(
            model_name='coach',
            name='userToCoach',
            field=models.ForeignKey(to='teachingMainApp.Learner', related_name='userToCoach'),
        ),
    ]
