from django.db import models

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
