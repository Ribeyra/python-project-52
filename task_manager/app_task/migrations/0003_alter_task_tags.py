# Generated by Django 5.0.6 on 2024-07-09 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tag', '0001_initial'),
        ('app_task', '0002_alter_task_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tasks', to='app_tag.tag'),
        ),
    ]