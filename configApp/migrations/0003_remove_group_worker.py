# Generated by Django 4.2.6 on 2023-10-24 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configApp', '0002_student_is_line'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='worker',
        ),
    ]
