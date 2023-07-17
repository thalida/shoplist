# Generated by Django 4.2.3 on 2023-07-17 02:28

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0012_remove_list_category_remove_list_is_hidden_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="storeproduct",
            name="aisle",
        ),
        migrations.CreateModel(
            name="StoreSection",
            fields=[
                (
                    "uid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=50)),
                (
                    "section_type",
                    models.CharField(
                        choices=[("aisle", "Aisle"), ("area", "Area")],
                        default="aisle",
                        max_length=10,
                    ),
                ),
                (
                    "store",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sections",
                        to="shop.store",
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="storeproduct",
            name="section",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="shop.storesection",
            ),
        ),
    ]
