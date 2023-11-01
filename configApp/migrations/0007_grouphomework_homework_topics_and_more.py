# Generated by Django 4.2.6 on 2023-10-30 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configApp', '0006_alter_group_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupHomeWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('descriptions', models.CharField(blank=True, max_length=500, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='configApp.group')),
            ],
        ),
        migrations.CreateModel(
            name='HomeWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(blank=True, max_length=5, null=True)),
                ('link', models.URLField()),
                ('is_active', models.BooleanField(default=False)),
                ('descriptions', models.CharField(blank=True, max_length=500, null=True)),
                ('groupHome', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='configApp.grouphomework')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='configApp.student')),
            ],
        ),
        migrations.CreateModel(
            name='Topics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('descriptions', models.CharField(blank=True, max_length=500, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='configApp.course')),
            ],
        ),
        migrations.RemoveField(
            model_name='levelnumber',
            name='group',
        ),
        migrations.RemoveField(
            model_name='levelnumber',
            name='level',
        ),
        migrations.RemoveField(
            model_name='levelnumber',
            name='student',
        ),
        migrations.DeleteModel(
            name='Level',
        ),
        migrations.DeleteModel(
            name='LevelNumber',
        ),
        migrations.AddField(
            model_name='grouphomework',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='configApp.topics'),
        ),
    ]