# Generated by Django 4.1.7 on 2023-04-26 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0006_table_groupname_priority_table_groups_priority"),
    ]

    operations = [
        migrations.AlterField(
            model_name="table_staff",
            name="id",
            field=models.CharField(
                max_length=8, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
