# Generated by Django 4.1.7 on 2023-05-06 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0011_table_date_holiday"),
    ]

    operations = [
        migrations.AlterField(
            model_name="table_shift",
            name="charactor",
            field=models.CharField(max_length=5, verbose_name="白夜班"),
        ),
    ]
