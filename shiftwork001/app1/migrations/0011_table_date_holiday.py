# Generated by Django 4.1.7 on 2023-05-06 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0010_table_rule_table_project_attend_rule"),
    ]

    operations = [
        migrations.AddField(
            model_name="table_date",
            name="holiday",
            field=models.BooleanField(default=False, verbose_name="假日"),
        ),
    ]