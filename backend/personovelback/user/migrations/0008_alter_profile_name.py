# Generated by Django 4.2.8 on 2024-04-03 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_profile_delete_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
    ]