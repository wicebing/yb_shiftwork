# Generated by Django 4.1.7 on 2023-04-25 16:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app1", "0004_alter_table_staff_authid"),
    ]

    operations = [
        migrations.AddField(
            model_name="table_groupname",
            name="turn",
            field=models.IntegerField(default=0, verbose_name="順序碼"),
        ),
        migrations.AlterField(
            model_name="table_class",
            name="date",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="app1.table_date",
                verbose_name="日期",
            ),
        ),
        migrations.AlterField(
            model_name="table_groups",
            name="groupname",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="app1.table_groupname",
                verbose_name="群組名稱",
            ),
        ),
        migrations.AlterField(
            model_name="table_groups",
            name="staff",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="app1.table_staff",
                verbose_name="人員",
            ),
        ),
        migrations.AlterField(
            model_name="table_meeting",
            name="date",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="app1.table_date",
                verbose_name="日期",
            ),
        ),
        migrations.AlterField(
            model_name="table_personal",
            name="date",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="app1.table_date",
                verbose_name="日期",
            ),
        ),
        migrations.AlterField(
            model_name="table_project",
            name="status",
            field=models.BooleanField(default=False, verbose_name="狀態"),
        ),
        migrations.AlterField(
            model_name="table_shift_schedule",
            name="date",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="app1.table_date",
                verbose_name="日期",
            ),
        ),
        migrations.AlterField(
            model_name="table_shift_schedule",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="app1.table_project",
                verbose_name="專案",
            ),
        ),
        migrations.AlterField(
            model_name="table_shift_schedule",
            name="shift",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="app1.table_shift",
                verbose_name="班別",
            ),
        ),
        migrations.AlterField(
            model_name="table_shift_schedule",
            name="staff",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="app1.table_staff",
                verbose_name="人員",
            ),
        ),
        migrations.AlterField(
            model_name="table_staff",
            name="AUTHid",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
                verbose_name="人員",
            ),
        ),
    ]