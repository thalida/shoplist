from django.db import models

class ListCategories(models.IntegerChoices):
    """
    List Category Choices
    """
    SHOPPING_LIST = 1
    RECIPE = 10

class StoreCategories(models.IntegerChoices):
    """
    Store Category Choices
    """
    GROCERY = 1

class ProductCategories(models.IntegerChoices):
    UNKNOWN = 0
    OTHER = 1

    PRODUCE = 10
    FRUIT = 11
    VEGETABLE = 12

    MEAT = 20
    DELI = 21
    SEAFOOD = 22

    BREAD = 30
    BAKERY = 31
    BAKING = 32

    DAIRY = 40

    FROZEN = 50

    CANNED = 60

    CONDIMENTS = 70

    BEVERAGE = 80

    SNACK = 90

    HEALTH = 100
    BEAUTY = 101

    HOME = 110

    OUTDOOR = 120


class Units(models.IntegerChoices):
    UNKNOWN = 0
    TBSP = 2
    TSP = 3
    CUP = 4
    QUART = 5
    GALLON = 6
    OZ = 7
    LB = 8
    PINT = 20
    GRAM = 21
    KG = 22
    ML = 23
    L = 24
