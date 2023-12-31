# Generated by Django 4.2.3 on 2023-07-11 15:50

from django.db import migrations


def add_choices(apps, schema_editor):
    ListCategory = apps.get_model("shop", "ListCategory")
    StoreCategory = apps.get_model("shop", "StoreCategory")
    ProductCategory = apps.get_model("shop", "ProductCategory")
    ProductUnit = apps.get_model("shop", "ProductUnit")

    ListCategory.objects.bulk_create([
        ListCategory(name="Shopping List"),
    ])

    StoreCategory.objects.bulk_create([
        StoreCategory(name="Grocery"),
    ])

    ProductCategory.objects.bulk_create([
        ProductCategory(name="Unknown"),
        ProductCategory(name="Other"),
        ProductCategory(name="Produce"),
        ProductCategory(name="Fruit"),
        ProductCategory(name="Vegetable"),
        ProductCategory(name="Meat"),
        ProductCategory(name="Deli"),
        ProductCategory(name="Seafood"),
        ProductCategory(name="Bread"),
        ProductCategory(name="Bakery"),
        ProductCategory(name="Baking"),
        ProductCategory(name="Dairy"),
        ProductCategory(name="Frozen"),
        ProductCategory(name="Canned"),
        ProductCategory(name="Condiments"),
        ProductCategory(name="Beverage"),
        ProductCategory(name="Snack"),
        ProductCategory(name="Health"),
        ProductCategory(name="Beauty"),
        ProductCategory(name="Home"),
        ProductCategory(name="Outdoor"),
    ])

    ProductUnit.objects.bulk_create([
        ProductUnit(name="Unknown"),
        ProductUnit(name="Tbsp"),
        ProductUnit(name="Tsp"),
        ProductUnit(name="Cup"),
        ProductUnit(name="Quart"),
        ProductUnit(name="Gallon"),
        ProductUnit(name="Oz"),
        ProductUnit(name="Lb"),
        ProductUnit(name="Pint"),
        ProductUnit(name="g"),
        ProductUnit(name="Kg"),
        ProductUnit(name="ml"),
        ProductUnit(name="L"),
    ])



class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0006_list_category_listproduct_unit_product_category_and_more"),
    ]

    operations = [
        migrations.RunPython(add_choices),
    ]
