# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc

import uuid
from rango.models import Category


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0002_auto_20151110_2357'),
    ]
    
    def gen_uuid(apps, schema_editor):
        for row in Category.objects.all():
            row.slug = uuid.uuid4()
            row.save()


    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=uuid.uuid4),
            preserve_default=True,
        ),
        migrations.RunPython(gen_uuid),

        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=uuid.uuid4, unique=True),
        ),
    ]
