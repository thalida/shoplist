import uuid

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from shop.choices import ColorChoice, SectionTypeChoice


class List(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)
    categories = models.ManyToManyField('ListCategory', blank=True, related_name='lists')
    products = models.ManyToManyField('Product', through='ListProduct', related_name='lists')

    def __str__(self):
        return self.name


class ListCategory(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)
    color = models.CharField(max_length=10, choices=ColorChoice.choices, default=ColorChoice.WHITE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('List Categories')


class ListProduct(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    list = models.ForeignKey('List', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity_have = models.IntegerField(default=0)
    quantity_needed = models.IntegerField(default=1)
    unit = models.ForeignKey('ProductUnit', blank=True, null=True, default=None, on_delete=models.SET_NULL)

    def __str__(self):
        return self.product.name


class Product(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)
    categories = models.ManyToManyField('ProductCategory', blank=True, related_name='products')

    def __str__(self):
        return self.name


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


class StoreSection(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=50)
    section_type = models.CharField(max_length=10, choices=SectionTypeChoice.choices, default=SectionTypeChoice.AISLE)

    def __str__(self):
        return self.name
