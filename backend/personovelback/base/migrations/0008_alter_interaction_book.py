# Generated by Django 5.0 on 2024-02-22 13:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_interaction_chapter_number_alter_interaction_chapter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interaction',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.book'),
        ),
    ]
