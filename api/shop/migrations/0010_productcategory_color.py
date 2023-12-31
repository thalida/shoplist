# Generated by Django 4.2.3 on 2023-07-13 04:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0009_alter_list_products_alter_store_products"),
    ]

    operations = [
        migrations.AddField(
            model_name="productcategory",
            name="color",
            field=models.CharField(
                choices=[
                    ("white", "White"),
                    ("gray", "Gray"),
                    ("black", "Black"),
                    ("red", "Red"),
                    ("orange", "Orange"),
                    ("yellow", "Yellow"),
                    ("green", "Green"),
                    ("blue", "Blue"),
                    ("purple", "Purple"),
                    ("pink", "Pink"),
                ],
                default="white",
                max_length=10,
            ),
        ),
    ]
