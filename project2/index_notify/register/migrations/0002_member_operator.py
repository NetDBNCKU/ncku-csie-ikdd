# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='operator',
            field=models.CharField(max_length=1, default='<'),
            preserve_default=False,
        ),
    ]
