# Generated by Django 4.2.3 on 2023-07-09 02:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="List",
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
                ("is_deleted", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
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
                    "category",
                    models.IntegerField(
                        choices=[
                            (0, "Unknown"),
                            (1, "Other"),
                            (10, "Produce"),
                            (11, "Fruit"),
                            (12, "Vegetable"),
                            (20, "Meat"),
                            (21, "Deli"),
                            (22, "Seafood"),
                            (30, "Bread"),
                            (31, "Bakery"),
                            (32, "Baking"),
                            (40, "Dairy"),
                            (50, "Frozen"),
                            (60, "Canned"),
                            (70, "Condiments"),
                            (80, "Beverage"),
                            (90, "Snack"),
                            (100, "Health"),
                            (101, "Beauty"),
                            (110, "Home"),
                            (120, "Outdoor"),
                        ],
                        default=0,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Store",
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
                ("category", models.IntegerField(choices=[(1, "Grocery")], default=1)),
            ],
        ),
        migrations.CreateModel(
            name="StoreProduct",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=5)),
                ("aisle", models.IntegerField(default=0)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="shop.product"
                    ),
                ),
                (
                    "store",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="shop.store"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="store",
            name="products",
            field=models.ManyToManyField(
                through="shop.StoreProduct", to="shop.product"
            ),
        ),
        migrations.CreateModel(
            name="ListProduct",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("quantity_needed", models.IntegerField(default=1)),
                ("quantity_have", models.IntegerField(default=0)),
                (
                    "unit",
                    models.IntegerField(
                        choices=[
                            (0, "Unknown"),
                            (2, "Tbsp"),
                            (3, "Tsp"),
                            (4, "Cup"),
                            (5, "Pint"),
                            (6, "Quart"),
                            (7, "Gallon"),
                            (8, "Oz"),
                            (9, "Lb"),
                            (10, "Gram"),
                            (11, "Kg"),
                            (12, "Ml"),
                            (13, "L"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "list",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="shop.list"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="shop.product"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="list",
            name="products",
            field=models.ManyToManyField(through="shop.ListProduct", to="shop.product"),
        ),
    ]
