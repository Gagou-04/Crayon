# Generated by Django 4.2.16 on 2024-09-26 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "high_level",
            "0003_alter_etape_machine_alter_etape_quantite_ressource_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="stock",
            name="usine",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="high_level.usine",
            ),
        ),
    ]
