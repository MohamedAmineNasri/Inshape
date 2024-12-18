# Generated by Django 4.2.16 on 2024-10-25 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routineplanner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Routine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_by', models.CharField(max_length=100)),
                ('details', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='note',
            name='workout',
        ),
        migrations.RemoveField(
            model_name='workout',
            name='schedule',
        ),
        migrations.DeleteModel(
            name='Exercise',
        ),
        migrations.DeleteModel(
            name='Note',
        ),
        migrations.DeleteModel(
            name='Schedule',
        ),
        migrations.DeleteModel(
            name='Workout',
        ),
    ]
