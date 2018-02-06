# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_assignment_position_papers(apps, schema_editor):
    Assignment = apps.get_model("core", "Assignment")
    PositionPaper = apps.get_model("core", "PositionPaper")
    queryset = Assignment.objects.all()

    for assignment in queryset:
        if not assignment.paper:
            paper = PositionPaper.objects.create()
            assignment.paper = paper
            assignment.save()


def create_committee_rubrics(apps, schema_editor):
    Rubric = apps.get_model("core", "Rubric")
    Committee = apps.get_model("core", "Committee")
    queryset = Committee.objects.all()

    for committee in queryset:
        if not committee.rubric:
            rubric = Rubric.objects.create()
            committee.rubric = rubric
            committee.save()


class Migration(migrations.Migration):

    dependencies = [('core', '0031_auto_20180201_0349'), ]

    operations = [
        migrations.RunPython(create_assignment_position_papers),
        migrations.RunPython(create_committee_rubrics)
    ]
