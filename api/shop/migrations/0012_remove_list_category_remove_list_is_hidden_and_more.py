# Generated by Django 4.2.3 on 2023-07-16 16:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0011_remove_product_category_product_categories_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="list",
            name="category",
        ),
        migrations.RemoveField(
            model_name="list",
            name="is_hidden",
        ),
        migrations.RemoveField(
            model_name="store",
            name="category",
        ),
        migrations.AddField(
            model_name="list",
            name="categories",
            field=models.ManyToManyField(
                blank=True, related_name="lists", to="shop.listcategory"
            ),
        ),
        migrations.AddField(
            model_name="listcategory",
            name="color",
            field=models.CharField(
                choices=[
                    ("white", "White"),
                    ("gray", "Gray"),
                    ("black", "Black"),
                    ("brown", "Brown"),
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
        migrations.AddField(
            model_name="store",
            name="categories",
            field=models.ManyToManyField(
                blank=True, related_name="stores", to="shop.storecategory"
            ),
        ),
        migrations.AddField(
            model_name="storecategory",
            name="color",
            field=models.CharField(
                choices=[
                    ("white", "White"),
                    ("gray", "Gray"),
                    ("black", "Black"),
                    ("brown", "Brown"),
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