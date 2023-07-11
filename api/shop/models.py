import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

class ListCategory(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('List Categories')

class StoreCategory(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Store Categories')

class ProductCategory(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)

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

class Product(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)
    category = models.ForeignKey('ProductCategory', blank=True, null=True, default=None, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Store(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)
    category = models.ForeignKey('StoreCategory', blank=True, null=True, default=None, on_delete=models.SET_NULL)
    products = models.ManyToManyField('Product', through='StoreProduct', related_name='stores')

    def __str__(self):
        return self.name


class StoreProduct(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    section = models.CharField(max_length=50, blank=True, null=True, default=None)
    aisle = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name


class List(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)
    category = models.ForeignKey('ListCategory', blank=True, null=True, default=None, on_delete=models.SET_NULL)
    products = models.ManyToManyField(Product, through='ListProduct', related_name='lists')

    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ListProduct(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    list = models.ForeignKey('List', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_have = models.IntegerField(default=0)
    quantity_needed = models.IntegerField(default=1)
    unit = models.ForeignKey('ProductUnit', blank=True, null=True, default=None, on_delete=models.SET_NULL)

    def __str__(self):
        return self.product.name
