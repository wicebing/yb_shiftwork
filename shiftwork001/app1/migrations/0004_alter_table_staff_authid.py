# Generated by Django 4.1.7 on 2023-04-18 03:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app1", "0003_alter_table_shift_schedule_staff"),
    ]

    operations = [
        migrations.AlterField(
            model_name="table_staff",
            name="AUTHid",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="人員",
            ),
        ),
    ]