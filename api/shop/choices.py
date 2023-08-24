from django.db import models

class ColorChoice(models.TextChoices):
    WHITE = 'white', 'White'
    GRAY = 'gray', 'Gray'
    BLACK = 'black', 'Black'
    BROWN = 'brown', 'Brown'
    RED = 'red', 'Red'
    ORANGE = 'orange', 'Orange'
    YELLOW = 'yellow', 'Yellow'
    GREEN = 'green', 'Green'
    BLUE = 'blue', 'Blue'
    PURPLE = 'purple', 'Purple'
    PINK = 'pink', 'Pink'
