import uuid

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from shop.choices import ColorChoice


class Pantry(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50, default='My Pantry')
    products = models.ManyToManyField('Product', through='PantryProduct', related_name='pantries')

    def __str__(self):
        return self.name


class PantryProduct(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    pantry = models.ForeignKey('Pantry', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    minimum_quantity = models.FloatField(default=1)
    unit = models.ForeignKey('ProductUnit', blank=True, null=True, default=None, on_delete=models.SET_NULL)
    buy_threshold = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        default=0.50,
    )
    expiration_date = models.DateField(blank=True, null=True, default=None)
    notes = models.TextField(blank=True, null=True, default=None)

    def __str__(self):
        return self.product.name

    class Meta:
        ordering = ['product__name']


class Recipe(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True, default=None)
    url = models.URLField(blank=True, null=True, default=None)

    categories = models.ManyToManyField('RecipeCategory', blank=True, related_name='recipes')
    products = models.ManyToManyField('Product', through='RecipeProduct', related_name='recipes')

    is_planned = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class RecipeCategory(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)
    color = models.CharField(max_length=10, choices=ColorChoice.choices, default=ColorChoice.WHITE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Recipe Categories')


class RecipeProduct(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.FloatField(default=1)
    unit = models.ForeignKey('ProductUnit', blank=True, null=True, default=None, on_delete=models.SET_NULL)
    notes = models.TextField(blank=True, null=True, default=None)

    def __str__(self):
        return self.product.name


class Product(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True, default=None)
    categories = models.ManyToManyField('ProductCategory', blank=True, related_name='products')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class ProductCategory(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)
    color = models.CharField(max_length=10, choices=ColorChoice.choices, default=ColorChoice.WHITE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Product Categories')


class ProductUnit(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=10, blank=True, null=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Product Units')


class Store(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)
    categories = models.ManyToManyField('StoreCategory', blank=True, related_name='stores')
    products = models.ManyToManyField('Product', through='StoreProduct', related_name='stores')

    def __str__(self):
        return self.name


class StoreCategory(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)
    color = models.CharField(max_length=10, choices=ColorChoice.choices, default=ColorChoice.WHITE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Store Categories')


class StoreSection(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True, default=None)
    section_type = models.ForeignKey('StoreSectionType', blank=True, null=True, default=None, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class StoreSectionType(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class StoreProduct(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=None)
    section = models.ForeignKey('StoreSection', blank=True, null=True, default=None, on_delete=models.SET_NULL)

    def __str__(self):
        return self.product.name

    def clean(self) -> None:
        if self.section and self.section.store != self.store:
            raise ValidationError('Section store must be the same as product store')

        return super().clean()

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        return super().save(*args, **kwargs)
