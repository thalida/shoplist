from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, TabularInline

from .models import (
    ListCategory,
    StoreCategory,
    ProductCategory,
    ProductUnit,
    Product,
    Store,
    StoreProduct,
    List,
    ListProduct,
)

@admin.register(ListCategory)
class ListCategoryAdmin(ModelAdmin):
    """
    ListCategory admin
    """
    pass


@admin.register(StoreCategory)
class StoreCategoryAdmin(ModelAdmin):
    """
    StoreCategory admin
    """
    pass

@admin.register(ProductCategory)
class ProductCategoryAdmin(ModelAdmin):
    """
    ProductCategory admin
    """
    pass


@admin.register(ProductUnit)
class ProductUnitAdmin(ModelAdmin):
    """
    ProductUnit admin
    """
    pass


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    """
    Product admin
    """
    pass


class StoreProductInline(TabularInline):
    """
    StoreProduct inline
    """
    model = StoreProduct
    extra = 0

@admin.register(Store)
class StoreAdmin(ModelAdmin):
    """
    Store admin
    """
    inlines = [
        StoreProductInline,
    ]


class ListProductInline(TabularInline):
    """
    ListProduct inline
    """
    model = ListProduct
    extra = 0


@admin.register(List)
class ListAdmin(ModelAdmin):
    """
    List admin
    """

    inlines = [
        ListProductInline,
    ]
