# Generated by Django 4.1.1 on 2023-08-06 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_profile_is_active_alter_profile_department_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='current_city',
            field=models.CharField(default='N', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='research_interest',
            field=models.CharField(default='N', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='room_no',
            field=models.CharField(default='N', max_length=200, null=True),
        ),
    ]
