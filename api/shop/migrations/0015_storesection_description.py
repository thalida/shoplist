# Generated by Django 4.2.3 on 2023-07-25 19:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0014_alter_storeproduct_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="storesection",
            name="description",
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
