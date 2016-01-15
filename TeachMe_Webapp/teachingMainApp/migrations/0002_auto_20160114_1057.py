# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachingMainApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coach',
            old_name='userToCoach',
            new_name='theUserToCoach',
        ),
    ]
