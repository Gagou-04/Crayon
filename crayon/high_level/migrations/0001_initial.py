# Generated by Django 4.2.16 on 2024-09-25 14:12

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Ville",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=100)),
                ("code_postal", models.IntegerField()),
                ("prix_m_2", models.IntegerField()),
            ],
        ),
    ]
