# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_member_operator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='operator',
        ),
    ]
