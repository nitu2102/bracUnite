# Generated by Django 4.2.3 on 2023-07-30 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0004_alter_profile_student_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="student_id",
            field=models.CharField(max_length=200, null=True),
        ),
    ]