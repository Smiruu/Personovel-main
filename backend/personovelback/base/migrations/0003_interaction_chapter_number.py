# Generated by Django 5.0 on 2024-02-22 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_remove_interaction_chapter_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='interaction',
            name='chapter_number',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]