# Generated by Django 4.1.7 on 2023-05-07 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0015_alter_table_extra_staff_extra_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="table_staff_extra",
            name="credit",
            field=models.IntegerField(default=0, verbose_name="超排分數"),
        ),
        migrations.AddField(
            model_name="table_staff_relax",
            name="credit",
            field=models.IntegerField(default=0, verbose_name="減班分數"),
        ),
    ]