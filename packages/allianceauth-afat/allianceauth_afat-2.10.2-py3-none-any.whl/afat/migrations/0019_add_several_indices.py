# Generated by Django 3.1.8 on 2021-05-01 22:25

# Django
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("eveonline", "0014_auto_20210105_1413"),
        ("afat", "0018_auto_20210420_2016"),
    ]

    operations = [
        migrations.AlterField(
            model_name="afat",
            name="afatlink",
            field=models.ForeignKey(
                help_text="The fatlink the character registered at",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="afats",
                to="afat.afatlink",
            ),
        ),
        migrations.AlterField(
            model_name="afat",
            name="character",
            field=models.ForeignKey(
                help_text="Character who registered this fat",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="afats",
                to="eveonline.evecharacter",
            ),
        ),
        migrations.AlterField(
            model_name="afat",
            name="shiptype",
            field=models.CharField(
                db_index=True,
                help_text="The ship the character was flying",
                max_length=100,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="afatlink",
            name="afattime",
            field=models.DateTimeField(
                db_index=True,
                default=django.utils.timezone.now,
                help_text="When was this fatlink created",
            ),
        ),
        migrations.AlterField(
            model_name="afatlink",
            name="hash",
            field=models.CharField(
                db_index=True, help_text="The fatlinks hash", max_length=254
            ),
        ),
        migrations.AlterField(
            model_name="afatlog",
            name="log_time",
            field=models.DateTimeField(
                db_index=True, default=django.utils.timezone.now
            ),
        ),
    ]
