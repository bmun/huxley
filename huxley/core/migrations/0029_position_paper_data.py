# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from huxley.core.models import Assignment, Committee, PositionPaper, Rubric


def create_assignment_position_papers(apps, schema_editor):
    queryset = Assignment.objects.all()

    for assignment in queryset:
        if not assignment.paper:
            paper = PositionPaper.objects.create()
            assignment.paper = paper
            assignment.save()


def create_committee_rubrics(apps, schema_editor):
    queryset = Committee.objects.all()

    for committee in queryset:
        if not committee.rubric:
            rubric = Rubric.objects.create()
            committee.rubric = rubric
            committee.save()


class Migration(migrations.Migration):

    dependencies = [('core', '0028_auto_20171229_1118'), ]

    operations = [
        migrations.RunPython(create_assignment_position_papers),
        migrations.RunPython(create_committee_rubrics)
    ]
